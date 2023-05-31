import pickle
import time
import os
from loguru import logger

from NextPageButtonExtractor.handler.utils.clac_feature import ClacFeature

real_path = os.path.dirname(__file__)

def load_classifier(algorithm='xgb'):
    logger.debug(f'当前加载的按钮分类模型为{algorithm}')
    with open(os.path.join(os.path.dirname(real_path),f'dataset_and_models/pickles/button_{algorithm}_156.pickle'),'rb') as f:
        button_classify = pickle.load(f)
    return button_classify
# button_classify = load_classifier('svm')

# button_classify = load_classifier('lg')
# button_classify = load_classifier('rfc')
button_classify = load_classifier()



class ButtonExtractor(ClacFeature):
    def __init__(self,html,text=True,**kwargs):
        super().__init__(html,text)
        self.html = html

    def predictButton(self):
        X = self.getX()
        return button_classify.predict(X)[0]

    def predictProbaButton(self):
        X = self.getX()
        return button_classify.predict_proba(X)[0][1]

def process(response,htmlsource=False):
    candais = response.xpath('.//*[string-length(.)<5 and not(*)]')
    logger.debug(f'候选元素的结果有{len(candais)}个')
    res_list = []
    for candi in candais:
        try:
            html = candi.extract()
            handler = ButtonExtractor(html)
            is_button = handler.predictButton()
            if is_button:
                if htmlsource:
                    res_list.append(html)
                else:
                    res_list.append(handler.getXpath())
        except Exception as e:
            logger.debug(e)
            pass
    logger.debug(f'分类后元素的结果有{len(res_list)}个')
    return list(set(res_list))

if __name__ == "__main__" :
    # print(real_path)
    # load_classifier()
    time1 = time.time()
    # text = '''<img src="../../images/ico_yellow.jpg" width="3" height="7" title="图片装饰" alt="图片装饰">'''
    text = '''<a class="n" href="/s?wd=%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C&amp;pn=10&amp;oq=%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C&amp;ie=utf-8&amp;usm=2&amp;rsv_pq=9ff114c100019241&amp;rsv_t=aba07Ltrd4bcj%2FNVsG1U5BF4CKZ7OSIdaGOXE0WRruJgB1rJhA%2FIPViWTns&amp;topic_pn=&amp;rsv_page=1" pcked="1">下一页 &gt;</a>'''
    handler = ButtonExtractor(text)
    poss = handler.predictProbaButton()
    res = handler.predictButton()
    Xpath = handler.getXpath()
    logger.info(f'{text}的分数为: {poss},判定为{res}，选择器为{Xpath}')