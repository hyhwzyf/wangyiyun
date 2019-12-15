import pymysql
from datetime import datetime 
from bs4 import BeautifulSoup
import requests
import json
import time
import random
import re

#grab playlists
cookies={
	'mail_psc_fingerprint':'',
	'_iuqxldmzr_':'32',
	'_ntes_nnid':'',
	'_ntes_nuid':'',
	'WM_TID':'',
	'usertrack':'ezq0ZVyhVd9DxWa/FuHcAg==',
	'vinfo_n_f_l_n3':'',
	'P_INFO':'',
	'hb_MA-9ADA-91BF1A6C9E06_source':'www.baidu.com',
	'WM_NI':'',
	'mp_MA-9ADA-91BF1A6C9E06_hubble':'',
	'JSESSIONID-WYYY':'',
	'WM_NIKE':''
}

headers={
	'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'accept-Encoding':'gzip, deflate, br',
	'accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'referer':'https://music.163.com/',
	'upgrade-insecure-requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

types=['语种','风格','情感','场景','主题']
topics=[['粤语'],
['R%26B%2FSoul','流行','摇滚','民谣','电子','舞曲','说唱','爵士','乡村','古典','民族','英伦','金属','朋克','蓝调','雷鬼','世界音乐','拉丁','古风','后摇','New Age','Bossa Nova'],
['怀旧','清新','浪漫','伤感','治愈','放松','孤独','感动','兴奋','快乐','安静','思念'],
['清晨','夜晚','学习','工作','午休','下午茶','地铁','驾车','运动','旅行','散步','酒吧'],
['70后','80后','90后','00后','儿童','校园']]
result=[]
for i in range(len(types)):
	for j in range(len(topics[i])):
		url='https://music.163.com/discover/playlist/?cat=%s'%topics[i][j]
		print(url)
		response=requests.get(url,cookies=cookies,headers=headers)
		html=response.text
		# print(html)
		soup=BeautifulSoup(html,'lxml')
		playlists=soup.select('.msk')
		for p in playlists:
			result.append([types[i],topics[i][j],str(p)[str(p).find('id=')+3:str(p).find('" title')],str(p)[str(p).find('title=')+7:str(p).find('"></a>')]])
# print(playlists)
# print(len(playlists))
print(len(result))

for i in result:
	connection=pymysql.connect(host='localhost',port=3306,user='root',password='sdfzg11b',db='wangyiyun',charset='utf8')
	cursor=connection.cursor()
	sql="insert into playlist(type,topic,plid,plname) values('%s','%s',%s,'%s')"%(i[0],i[1],i[2],i[3].replace("'",'"'))
	print(sql)
	cursor.execute(sql)
	cursor.close()
	connection.commit()

connection.close()
