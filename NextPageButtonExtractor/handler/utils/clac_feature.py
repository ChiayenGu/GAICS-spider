import re
import pandas as pd
from lxml import etree
from collections import defaultdict
from loguru import logger

button_tag_name_list = ['a', 'li', 'span', 'button', 'div']
not_button_tag_name_list = ['img','style','script','meta','head','title','link']
parser = etree.HTMLParser(encoding="utf-8")

class ClacFeature:
    def __init__(self,html,text=True):
        self.HTML = etree.XML(html,parser=parser).xpath('/html/body/*')[0] if text else html
        self.htmlRes = etree.tounicode(self.HTML)
        self.attr = defaultdict(str)
        self.node = defaultdict(str)
        self.mergedAttr = ''
        self.feature = defaultdict(int)
        self._mergeAttr()
        self._addInit()
        self.clacFeature()

    def _returnNull(self):
        return ''

    def _getAttrs(self):
        return self.HTML.items()

    def _addAttrsToSelf(self):
        for name,value in self._getAttrs():
            self.attr.update({name:value})

    def _mergeAttr(self):
        self._addAttrsToSelf()
        self.mergedAttr = ' '.join(list(self.attr.values()))


    def _addInit(self):
        self.node['text'] = self.HTML.text or ''
        self.node['tagName'] = self.HTML.tag

    def _clacTextNum(self):
        # 文字字数
        return len(self.node['text'])

    def _clacTextMatchPoint(self):
        # 文字内容与特定字符的匹配程度
        # 下一页 等： 10
        # > : 2
        nextPageMatch = 10 if re.search('下.?页|next[\S\s]?page',self.node['text'],re.IGNORECASE) else 0
        nextPageSymbolMatch = 2 if re.search('(?<!>)>(?!>)',self.node['text'],re.IGNORECASE) else 0
        return max(nextPageMatch,nextPageSymbolMatch)

    def _clacAttrMatchPoint(self):
        if len(self.mergedAttr) == 0:
            return 0
        nextPageMatch = 10 if re.search('下.?页|next[\S\s]?page|page[\s\S]?next|next[\s\S]?pg|pg[\s\S]?next',self.mergedAttr,re.IGNORECASE) else 0
        nextPageSymbolMatch = 5 if re.search('next|pag|pg|&gt;',self.mergedAttr,re.IGNORECASE) else 0
        btnMatch = 2 if re.search('btn|button',self.mergedAttr,re.IGNORECASE) else 0
        return max(nextPageMatch,nextPageSymbolMatch,btnMatch)

    def _clacTagMatchPoint(self):
        tagMatchPoint = 5 if self.node['tagName'] in button_tag_name_list else 0
        tagMatchPoint = -100 if self.node['tagName'] in not_button_tag_name_list else tagMatchPoint
        return tagMatchPoint

    def _clacEvent(self):
        return 1 if 'onclick' in self.attr.keys() else 0

    def _clacHref(self):
        href = self.attr['href']
        if not href:
            return 0
        hasHref = 1 if href else 0
        javaScirptMatch = 2 if re.search('javascript',href,re.IGNORECASE) else 0
        if javaScirptMatch:
            return javaScirptMatch
        htmlMatch = 1 if re.search('\.s?html',href,re.IGNORECASE) else 0
        htmlMatch2 = 3 if re.search('\d\.s?html',href,re.IGNORECASE) else 0
        return max(htmlMatch,hasHref)

    def getX(self):
        X = [[self.feature['textNum'],
                      self.feature['textMatchPoint'],
                      self.feature['attrMatchPoint'],
                      self.feature['tagMatchPoint'],
                      self.feature['event'],
                      self.feature['hrefPoint']
                      ]]
        return X

    def getXpath(self):
        attrs = []
        for key in self.attr.keys():
            value = self.attr[key]
            if key in ['class', 'title', 'id'] and value:
                attrs.append(f'@{key}="{value}"')

        attrSec = ' and '.join(attrs) if len(attrs) else ''
        textContains = 'text()="{text}"'.format(text=self.node['text']) if self.node['text'] else ''
        if attrSec and textContains:
            xpath = f'[{attrSec} and {textContains}]'
        elif not attrSec and not textContains:
            xpath = ''
        else:
            xpath = f'[{attrSec if attrSec else textContains}]'
        return './/{tagName}{xpath}'.format(tagName=self.node['tagName'], xpath=xpath)

    def clacFeature(self):
        self.feature.update({
            'textNum': self._clacTextNum(),
            'textMatchPoint': self._clacTextMatchPoint(),
            'attrMatchPoint': self._clacAttrMatchPoint(),
            'tagMatchPoint': self._clacTagMatchPoint(),
            'event': self._clacEvent(),
            'hrefPoint':self._clacHref()
        })


def clacFeatureForText(text):
    try:
        handler = ClacFeature(text)
        return handler.feature
    except:
        logger.warning("格式化失败{text}".format(text=text))
        return {
            'textNum': 0,
            'textMatchPoint': 0,
            'attrMatchPoint':0,
            'tagMatchPoint': 0,
            'event': 0,
            'hrefPoint': 0
        }



if __name__ =="__main__":
    dataset = pd.read_csv('../dataset/dataset.csv')
    res = []
    for line in dataset.itertuples():
        feature = clacFeatureForText(line.html)
        feature.update({'html':line.html,'lable':line.next_button})
        res.append(feature)
    newFrame = pd.DataFrame(res)
    newFrame.to_csv('../dataset/dataset_with_feature.csv')
    # data = pd.read_csv('dataset_with_feature.csv')

    # print(data.iloc[:, 1:7])