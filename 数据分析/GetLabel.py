# coding=utf-8
import pandas as pd
import pickle

# 分词
import jieba.posseg as pseg

import sys
import importlib

importlib.reload(sys)

stopwords = [line.rstrip() for line in open('chineseStopWords.txt')]
stopwords[:10]


def cut(txt):
    result = ''
    try:
        for w in pseg.cut(txt):
            seg = w.word
            if seg not in stopwords:
                result += seg + ' '
    except:
        pass
    return result

# 读取全样本数据
DataSet_total = pd.read_csv('data2.csv', encoding = "utf-8",header=0)
# 处理全样本中的缺失值
# 清洗全样本数据
# 保存清洗后的全样本

try:
    DataSet_total['availble']
except:
    DataSet_total['availble'] = DataSet_total.lyric.apply(cut)

DataSet_total['availble'] = DataSet_total['availble'].fillna('')

with open('Motion.pkl', 'rb') as f:
    Model_Motion = pickle.load(f)
with open('FeaTrain_Motion.pkl', 'rb') as f:
    Feature_train_Motion = pickle.load(f)
#with open('Place.pkl', 'rb') as f:
 #   Model_Place = pickle.load(f)
#with open('FeaTrain_Place.pkl', 'rb') as f:
 #   Feature_train_Place = pickle.load(f)
with open('Style.pkl', 'rb') as f:
    Model_Style = pickle.load(f)
with open('FeaTrain_Style.pkl', 'rb') as f:
    Feature_train_Style = pickle.load(f)
with open('Audience.pkl', 'rb') as f:
    Model_Audience = pickle.load(f)
with open('FeaTrain_Audience.pkl', 'rb') as f:
    Feature_train_Audience = pickle.load(f)
with open('Yueyu.pkl', 'rb') as f:
    Model_Yueyu = pickle.load(f)
with open('FeaTrain_Yueyu.pkl', 'rb') as f:
    Feature_train_Yueyu = pickle.load(f)

Vector_total_Motion = Feature_train_Motion.transform(DataSet_total['availble'])
#Vector_total_Palce = Feature_train_Place.transform(DataSet_total['availble'])
Vector_total_Style = Feature_train_Style.transform(DataSet_total['availble'])
Vector_total_Audience = Feature_train_Audience.transform(DataSet_total['availble'])
Vector_total_Yueyu = Feature_train_Yueyu.transform(DataSet_total['availble'])

# 分类 情感
DataSet_total['情感'] = Model_Motion.predict(Vector_total_Motion)
print("情感标签已分类完成！")

#分类 场景
#DataSet_total['场景'] = Model_Place.predict(Vector_total_Palce)
#print("场景标签已分类完成！")

#分类 风格
DataSet_total['风格'] = Model_Style.predict(Vector_total_Style)
print("风格标签已分类完成！")

#分类 听众
DataSet_total['听众'] = Model_Audience.predict(Vector_total_Audience)
print("听众标签已分类完成！")

#分类 粤语
DataSet_total['粤语'] = Model_Yueyu.predict(Vector_total_Yueyu)
print("粤语标签已分类完成！")

DataSet_total.to_csv('LabelResult.csv', index=None, encoding='gb18030')


