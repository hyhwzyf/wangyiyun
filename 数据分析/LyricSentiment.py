#歌词情感分析
#通过调用百度情感分析API接口

'''
API调用说明

请求参数
参数	类型	描述
text	string	文本内容，最大2048字节度

返回参数
参数	说明	描述
log_id	uint64	请求唯一标识码
sentiment	int	表示情感极性分类结果，0:负向，1:中性，2:正向
confidence	float	表示分类的置信度，取值范围[0,1]
positive_prob	float	表示属于积极类别的概率 ，取值范围[0,1]
negative_prob	float	表示属于消极类别的概率，取值范围[0,1]

注：
1. 实际调用时发现，文本含有分号和不含分号对结果影响非常大，有的结果直接从正向变成了负向，分析时清除掉文本中的非中文符号
2. 为便于后续进一步分析，情感极性分类改为-1,0,1表示
'''


import urllib3
import json
import time
import pandas as pd
import numpy as np
import os

file = pd.read_csv('lyic.csv',encoding="utf8",low_memory=False) #歌词文件
local_main2 = r'lyricsentimet.csv'  #结果文件


data = pd.DataFrame(columns = ['seq_num', 'singer_type', 'singer', 'music_title', 'date', 'comments', 'music_id', 'lyric', 'labels','label_prediction'])
data.to_csv(local_main2, index = None, encoding = 'utf_8_sig')

access_token='换上自己的'  #填自己的access_token
http=urllib3.PoolManager()
url='https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token='+access_token
df = pd.DataFrame(file)
#print(df)

labels =[]
label_prediction =[]

n = len(df) # n=233243

for i in range(n):
    
    if i%50 == 0:
        print("\r进度：{:.2f}%".format(100*i/n),end="") #虽然这句没啥用，但必须加上，要不等待太让人崩溃了，在.exe运行体验极佳。
    
    document = df[i:i+1]
    #print(document)
    seq_num = document['seq_num'][i]
    singer_type = document['singer_type'][i]
    singer = document['singer'][i]
    music_title = document['music_title'][i]
    date = document['date'][i]
    comments = document['comments'][i]
    music_id = document['music_id'][i]
    #lyric = document['lyric'][i]
    lyric = str(document['lyric'][i]).replace(";","").replace("?","")
    #print(lyric)
    
    #API调用有字符数限制，2048字节，也就是1024个汉字，保守起见，如果lyric字符数超过1000字符，只取前1000个字符进行计算
    if len(lyric)>1000:
        lyric = lyric[:1000]
    
    #测试一下有没有正确读取数据 
    '''
    print(seq_num,'\n',
          singer_type,'\n',
          singer,'\n',
          music_title,'\n',
          date,'\n',
          comments,'\n',
          music_id,'\n',lyric)
    '''
    if (i+1)%20==0:
        time.sleep(0.1)
        
    if lyric =='\n':
        lyric = 'NA'
    params = {'text':lyric}

    encoded_data = json.dumps(params).encode('GBK')
    request=http.request('POST', 
                          url,
                          body=encoded_data,
                          headers={'Content-Type':'application/json'})
    result = str(request.data,'GBK')
    a =json.loads(result)
    #print(a)
    a1 =a['items'][0]
    #print(a1)
    labels.append(a1['sentiment'])#分类结果
    label_prediction.append(a1['positive_prob'])#展示的概率

    data1 = pd.DataFrame({'seq_num':seq_num,
                          'singer_type':singer_type,
                          'singer':singer,
                          'music_title':music_title,
                          'date':date,
                          'comments':comments,
                          'music_id':music_id,
                          'lyric':lyric, 
                          'labels':labels[i]-1,  
                          'label_prediction':label_prediction[i]},
                         columns = ['seq_num',
                                    'singer_type',
                                    'singer',
                                    'music_title',
                                    'date',
                                    'comments',
                                    'music_id',
                                    'lyric',
                                    'labels',
                                    'label_prediction'], index=[0])
    data1.to_csv(local_main2, index = None, mode = 'a', header = None, sep = ',', encoding = "utf_8_sig")
