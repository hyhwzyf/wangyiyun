# coding=utf-8
import pandas as pd
import numpy as np
import os
import math

import pickle

# 作图相关
import matplotlib.pyplot as pplt

# 分词
import jieba.posseg as pseg

# 文本特征提取:计数向量  /  tf-idf向量
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# 随机森林分类器
from sklearn.ensemble import RandomForestClassifier
# 逻辑回归
from sklearn.linear_model import LogisticRegression
# 非负矩阵分解：大矩阵分成两个小矩阵，降维，压缩
from sklearn.decomposition import NMF

# 数据集上随机划分出一定比例的训练集和测试集  /   K折交叉验证
from sklearn.model_selection import train_test_split, cross_val_score

# 多标签二值化
from sklearn.preprocessing import MultiLabelBinarizer

# 多分类转化成二分类，用一个分类器对应一个类别， 每个分类器都把其他全部的类别作为相反类别看待
from sklearn.multiclass import OneVsRestClassifier

# 朴素贝叶斯（伯努利分布，高斯分布，多项式分布）
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB

# 支持向量机做二分类
from sklearn.svm import SVC

# 评价分类模型的好坏，ROC灵敏度曲线
from sklearn.metrics import roc_curve

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


# 读入已清洗完的数据,要运行 pip3.7 install xlrd
DataSet_train = pd.read_csv('粤语.csv', encoding = "utf-8",header=0)
#DataSet_train = pd.read_csv('情感.csv', encoding = "utf-8",header=0)
#DataSet_train = pd.read_csv('风格.csv', encoding = "utf-8",header=0)
#DataSet_train = pd.read_csv('听众.csv', encoding = "utf-8",header=0)

DataSet_lyric = DataSet_train['歌词']
try:
    DataSet_train['availble']
except:
    DataSet_train['availble'] = DataSet_train.歌词.apply(cut)

DataSet_train['availble'] = DataSet_train.歌词.fillna('')

# 提取训练集文本特征
Feature_train = TfidfVectorizer(ngram_range=(1, 2))
Vector_feature_train = Feature_train.fit_transform(DataSet_train['availble'])

model = OneVsRestClassifier(RandomForestClassifier(), n_jobs=2)

# 学习标签 粤语
Vector_TargetLabel_train = DataSet_train['是否粤语']
model.fit(Vector_feature_train, Vector_TargetLabel_train)
with open('Yueyu.pkl','wb')as f:
    pickle.dump(model, f)
with open('FeaTrain_Yueyu.pkl','wb')as f1:
    pickle.dump(Feature_train,f1)

'''
# 学习标签 情感
Vector_TargetLabel_train = DataSet_train['情感']
model.fit(Vector_feature_train, Vector_TargetLabel_train)
with open('Motion.pkl','wb')as f:
    pickle.dump(model, f)
with open('FeaTrain_Motion.pkl','wb')as f1:
    pickle.dump(Feature_train,f1)
'''
'''
# 学习标签 听众
Vector_TargetLabel_train = DataSet_train['听众']
model.fit(Vector_feature_train, Vector_TargetLabel_train)
with open('Audience.pkl','wb')as f:
    pickle.dump(model, f)
with open('FeaTrain_Audience.pkl','wb')as f1:
    pickle.dump(Feature_train,f1)
'''
'''
# 学习标签 风格
Vector_TargetLabel_train = DataSet_train['风格']
model.fit(Vector_feature_train, Vector_TargetLabel_train)
with open('Style.pkl','wb')as f:
    pickle.dump(model, f)
with open('FeaTrain_Style.pkl','wb')as f1:
    pickle.dump(Feature_train,f1)
'''
#交叉验证
for Model_ in [RandomForestClassifier(), LogisticRegression(), SVC(), BernoulliNB()]:
    print(cross_val_score(OneVsRestClassifier(Model_), Vector_feature_train, Vector_TargetLabel_train))

DataSet_train.to_csv('LyricTrain.csv', index=None, encoding='gb18030')
