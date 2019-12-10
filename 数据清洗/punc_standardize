import pymysql

connection=pymysql.connect(host='localhost',port=3306,user='root',password='1111111',db='wangyiyun',charset='utf8')
cursor=connection.cursor()
sql='select songid,lyric from lyric2'
cursor.execute(sql)
cursor.close()
connection.commit()
ret=cursor.fetchall()
lyrics=[]
for item in ret:
    lyrics.append(item)
#歌词中的符号处理
#连续符号变单个符号与符号变';'同时进行。这里考虑了中文的常用符号以及英文的常用符号，就不用考虑全角半角了
import string 
from zhon.hanzi import punctuation as punc
punc=punc+string.punctuation+'！？，。；·：、——'
result=[]
for i in range(len(lyrics)):
    s = lyrics[i][1]
    for j in range(0,len(s)):
        if j >= len(s)-1:
            break
        if s[j] in punc:
            s = s[:j] + ';' + s[j+1:]
            while True:
                if j == len(s)-1:
                    break
                if s[j+1] in punc:
                    if j+2>=len(s):
                        s = s[:j+1]
                        break
                    else:
                        s = s[:j+1] + s[j+2:]
                else:
                    break
    # result.append([lyrics[i][0],s])
    sql="insert into lyric3(songid,lyric) values(%s,'%s')"%(lyrics[i][0],s)
    cursor=connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.commit()
connection.close()

print(len(result))
