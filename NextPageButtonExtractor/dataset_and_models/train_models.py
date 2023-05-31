import numpy as np
import pickle
from sklearn.metrics import accuracy_score,recall_score, f1_score,precision_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
import xgboost as xgb
from NextPageButtonExtractor.dataset_and_models import load_button
from loguru import logger

# 载入数据集
button = load_button.load_button()

def preprocess(data):
    X = data['data']
    y = data['target']

    m = len(X)
    # 确定随机种子
    np.random.seed(5)
    # 生成随机序列
    o = np.random.permutation(m)
    # 洗牌
    X = X[o]
    y = y[o]
    d = int(0.7 * m)
    X_train,X_test = np.split(X,[d])
    y_train,y_test = np.split(y,[d])
    return X,y,X_train,X_test,y_train,y_test

#获得训练集与测试集

X,y,X_train,X_test,y_train,y_test = preprocess(button)

# 创建四种模型
model_lg = LogisticRegression()
model_svm = svm.SVC(C=1,kernel='linear',probability=True)
model_xgb = xgb.XGBClassifier(objective="binary:logitraw", random_state=34)
model_rfc = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)

# 调用fit函数训练模型
model_lg.fit(X_train, y_train)
model_svm.fit(X_train,y_train)
model_xgb.fit(X_train, y_train)
model_rfc.fit(X_train, y_train)

def clac_score(model,model_name=''):
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    # print(f'{model_name} acc: {accuracy}  recall: {recall}, F1-score:{f1}')
    logger.debug(f'{model_name} acc: {accuracy}  recall: {recall}, F1-score:{f1}')

def save_model(model,model_name=''):
    with open(f'./pickles/button_{model_name}_156.pickle','wb+') as f:
        pickle.dump(model,f)

def procress():
    models = [model_lg,model_svm,model_rfc,model_xgb]
    models_names = ['lg','svm','rfc','xgb']

    for model in zip(models,models_names):
        clac_score(model[0],model[1])
        save_model(model[0],model[1])

if __name__ == '__main__':
    procress()