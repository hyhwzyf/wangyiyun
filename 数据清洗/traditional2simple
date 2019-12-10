import pymysql

connection=pymysql.connect(host='localhost',port=3306,user='root',password='1111111',db='wangyiyun',charset='utf8')
cursor=connection.cursor()
sql='select songid,lyric from lyric1'
cursor.execute(sql)
cursor.close()
connection.commit()
ret=cursor.fetchall()
lyrics=[]
for item in ret:
    lyrics.append(item)
# print(lyrics)

#简繁切换
# https://www.cnblogs.com/tangxin-blog/p/5616415.html
# coding:utf-8
from langconv import *
import sys
# 转换繁体到简体 t-s
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line
for i in lyrics:
    try:
        sql="insert into lyric2(songid,lyric) values(%s,'%s')"%(i[0],cht_to_chs(i[1]))
        # print(sql)
        cursor=connection.cursor()
        cursor.execute(sql)
        cursor.close()
        connection.commit()
    except Exception as e:
        print(e)
connection.close()
