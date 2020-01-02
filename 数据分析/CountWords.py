#计算当年歌曲中，歌词词频
#返回结果，词语word，词频count,比例ratio

import jieba
import math
import pandas as pd
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('chinesestopwords.txt',encoding='UTF-8').readlines()]
    return stopwords
stopwords = stopwordslist()

for y in range(1999,2020):
    year = str(y)
    print(year)
    local_main = 'wordcounts' + year +'.csv'
    file = pd.read_csv(year + '.csv',encoding='utf8')
    data = pd.DataFrame(columns = ['words','counts','ratios','years'])
    data.to_csv(local_main, index = None, encoding = 'utf_8_sig')
    df = pd.DataFrame(file)
    #print(df)

    counts = {}

    print("————————正在计算词频————————")
    n = len(df)
    for i in range(n):
        if i%50 == 0:
            print("\r进度：{:.2f}%".format(100*i/n),end="") 
        document = df[i:i+1]
        #print(document)
        lyric = str(document['lyric'][i]).replace(";","").replace("13","")
        #print(lyric)
        words = jieba.lcut(lyric)
        for word in words:
            if word.strip() not in stopwords and word !='\t' and word != '\r\n':
                counts[word] = counts.get(word, 0) + 1
    print("————————词频计算完毕————————")
    #print(counts.keys())

    total_word_counts = sum(counts.values())
    items = list(counts.items())
    items.sort(key = lambda x:x[1], reverse = True)
    #print(items)
    
    #计算写入词频概率
    word_count_results=[]
    for i in range(len(items)):
        word_count_result=[0,0,0,year]
        word_count_result[0] = items[i][0]  #word
        word_count_result[1] = items[i][1]  #count
        word_count_result[2] = math.log(items[i][1] / total_word_counts)  #ratio
        word_count_results.append(word_count_result)
    
    print("————————正在写入数据到csv文件————————")
    column_name=["words","counts","ratios","years"]
    data1=pd.DataFrame(columns=column_name,data=word_count_results)
    data1.to_csv(local_main, index = None, mode = 'a', header = None, sep = ',', encoding = "utf_8_sig")
    #逐条计算逐条写入当数据量很大时速度很慢，写入操作太多，需要考虑全部计算完毕后一次性写入
    print("————————数据写入完毕————————")   

    #看看分词频率排序情况
    '''
    for i in range(100):
        word, count = items[i]
        print("{0:<10}{1:>5}".format(word,count))
    

    #生成词云图
    print("————————正在生成词云图————————")
    mask = np.array(Image.open('0.jpg'))
    wc = wordcloud.WordCloud(font_path = "msyh.ttc",
                             max_words = 500,
                             background_color = "white")
    wc.generate_from_frequencies(counts)
    wc.to_file("H:\python\lyricAnalyse\wordcount\wordcloud\wordcloud"+year+".png")
    print("————————词云图生成完毕————————")
    #plt.imshow(wc)
    #plt.show()
    '''
