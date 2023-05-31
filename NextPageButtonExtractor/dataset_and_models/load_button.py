import numpy as np
from sklearn.utils import Bunch
import pandas as pd

def load_button():
    data_csv = pd.read_csv('dataset_with_feature.csv')
    button = Bunch()
    button.data = _get_button_data(data_csv)
    button.target = _get_button_target(data_csv)
    button.DESCR = _get_button_descr(data_csv)
    button.feature_names = _get_feature_names()
    button.target_name = _get_target_names()
    return button

def _get_button_data(data):
    """
    获取按钮特征值
    :return:
    """
    data_r = data.iloc[:, 1:7]
    data_np = np.array(data_r)
    return data_np


def _get_button_target(data):
    """
    获取按钮目标值
    :return:
    """
    data_b = data.iloc[:, 8:9]
    data_np = np.array(data_b).flatten()
    return data_np


def _get_button_descr(data):
    """
    获取数据集描述
    :return:
    """
    text = "本数据集为政府公告类列表页下一页按钮数据，样本数量：{}；" \
           "特征数量：{}；目标值数量：{}；无缺失数据" \
           "".format(data.index.size, data.columns.size - 2, 1)
    return text


def _get_feature_names():
    """
    获取特征名字
    :return:
    """
    fnames = ['textNum' , 'textMatchPoint', ' attrMatchPoint' , 'tagMatchPoint',  'event',  'hrefPoint']
    return fnames


def _get_target_names():
    """
    获取目标值名称
    :return:
    """
    tnames = ["next_page_button"]
    return tnames

if __name__ == "__main__":
    print(load_button())