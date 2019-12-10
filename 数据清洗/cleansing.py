#数据清理
#从mysql读取数据
import pymysql

connection=pymysql.connect(host='localhost',port=3306,user='root',password='11111111',db='wangyiyun',charset='utf8')
cursor=connection.cursor()
sql='select distinct songid,lyric from lyric'
cursor.execute(sql)
cursor.close()
connection.commit()
ret=cursor.fetchall()
lyrics=[]
for item in ret:
    lyrics.append(item)
# print(lyrics)

# 导入数据库文件为list格式，大的list为lyrics[]，其中的每个元素也为list，内容为[songid,lyric]

#清除大部分为英文的（定义为英文+字符总数>50%）
#https://blog.csdn.net/guotong1988/article/details/80896663
import string 
punc=string.punctuation
punc=punc+'，。；《》——'
del_items=[]
for i in range(len(lyrics)):
    notch=0     #非中文字符数 not chinese
    for j in lyrics[i][1]:
        if not (j >= u'\u4e00' and j <=u'\u9fa5'):  #中文的unicode码（包含简繁体，但是不包含台湾的注音）
            if j not in punc:
                notch = notch + 1   #统计非中文的字符数
    if notch/len(lyrics[i][1]) > 0.5:
        del_items.append(lyrics[i][0])
print(len(del_items))
for i in del_items:
    sql="delete from lyric where songid=%s"%i
    print(sql)
    cursor=connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.commit()
connection.close()

