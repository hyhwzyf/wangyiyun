import pymysql
from datetime import datetime 
from bs4 import BeautifulSoup
import requests
import json
import time
import random

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
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control':'max-age=0',
	'Host':'music.163.com',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}


# #获取华语歌手列表
# slist={1001:'"男歌手"',1002:'"女歌手"',1003:'"乐队/组合"'}
# pagelist=[-1,0]+list(range(65,91))
# singer=[]
# for s in slist:
# 	for p in pagelist:
# 		url='https://music.163.com/discover/artist/cat?id=%d&initial=%d'%(s,p)
# 		response=requests.get(url,cookies=cookies,headers=headers)
# 		html=response.text
# 		soup=BeautifulSoup(html,'lxml')
# 		msk=soup.select('.msk')
# 		for i in msk:
# 			singer.append([str(i)[str(i).find('id=')+3:str(i).find('" title')],s])
# 		sml=soup.select('.sml')
# 		for i in sml:
# 			item=str(i.select('a')[0])
# 			singer.append([item[item.find('id=')+3:item.find('" title')],s])

# connection=pymysql.connect(host='localhost',port=3306,user='root',password='11111111',db='wangyiyun',charset='utf8')
# for i in singer:
# 	i[1]=slist[i[1]]
# 	cursor=connection.cursor()
# 	sql='insert into singer(singerid,singertype) values(%s,%s)'%(i[0],i[1])
# 	print(sql)
# 	cursor.execute(sql)
# 	cursor.close()
# 	connection.commit()
# connection.close()


# #获取专辑
# connection=pymysql.connect(host='localhost',port=3306,user='root',password='11111111',db='wangyiyun',charset='utf8')
# singers=[]
# ext_singers=[]
# cursor=connection.cursor()
# sql='select singerid from singer where singerid not in (select singerid from album group by singerid)'
# cursor.execute(sql)
# connection.commit()
# sgr=cursor.fetchall()
# cursor.close()
# for i in sgr:
# 	singers.append(i[0])
# print(singers)

# for i in singers:
# 	url='https://music.163.com/artist/album?id=%s&limit=50'%i
# 	response=requests.get(url,cookies=cookies,headers=headers)
# 	html=response.text
# 	soup=BeautifulSoup(html,'lxml')
# 	msk=soup.select('.msk')
# 	for j in msk:
# 		print(j)
# 		cursor=connection.cursor()
# 		sql='insert into album(albumid,singerid) values(%s,%s)'%(str(j)[str(j).find('id=')+3:str(j).find('"><')],i)
# 		print(sql)
# 		cursor.execute(sql)
# 		cursor.close()
# 		connection.commit()
# 	time.sleep(1+random.random())
# connection.close()


#获取歌手名
connection=pymysql.connect(host='localhost',port=3306,user='root',password='11111111',db='wangyiyun',charset='utf8')
singers=[]
cursor=connection.cursor()
sql='select singerid from singer where singername is null'
cursor.execute(sql)
connection.commit()
sgr=cursor.fetchall()
for i in sgr:
	singers.append(i[0])
print(singers)
for i in singers:
	url='https://music.163.com/artist/album?id=%s&limit=50'%i
	response=requests.get(url,cookies=cookies,headers=headers)
	html=response.text
	soup=BeautifulSoup(html,'lxml')
	name=soup.select('title')[0].text
	name=name[:name.find(' - ')]
	if '（' in name:
		name=name[:name.find('（')]
	print(name)
	cursor=connection.cursor()
	sql='update singer set singername="%s" where singerid=%s'%(name,i)
	print(sql)
	cursor.execute(sql)
	cursor.close()
	connection.commit()
connection.close()


#获取歌曲id
connection=pymysql.connect(host='localhost',port=3306,user='root',password='11111111',db='wangyiyun',charset='utf8')
albums=[]
cursor=connection.cursor()
sql='select albumid from album where albumid not in (select albumid from song group by albumid)'
cursor.execute(sql)
connection.commit()
abm=cursor.fetchall()
cursor.close()
for i in abm:
	albums.append(i[0])
albums.remove('28412')
print(albums)

for i in albums:
	url='https://music.163.com/album?id=%s'%i
	response=requests.get(url,cookies=cookies,headers=headers)
	html=response.text
	soup=BeautifulSoup(html,'lxml')
	title=soup.select('.f-ff2')[0].text
	time=''
	company=''
	comment=0
	if len(soup.select('.intr'))>1:
		time=soup.select('.intr')[1].text.replace('发行时间：','')
	if len(soup.select('.intr'))>2:
		company=soup.select('.intr')[2].text.replace('发行公司：','').strip()
	if len(soup.select('.n-cmt'))>0:
		comment=soup.select('.n-cmt')[0]['data-count']
	if len(title)>30:
		title=title[:30]
	if len(company)>40:
		company=company[:40]
	cursor=connection.cursor()
	if '"' in title and "'" in title:
		pass
	else:
		if '"' in title:
			sql='update album set albumname=\'%s\',time="%s",company="%s",albumcomment="%s" where albumid=%s'%(title,time,company,comment,i)
		else:
			sql='update album set albumname="%s",time="%s",company="%s",albumcomment="%s" where albumid=%s'%(title,time,company,comment,i)
	print(sql)
	cursor.execute(sql)
	cursor.close()
	connection.commit()
	if len(soup.select('#song-list-pre-data'))>0:
		songs=soup.select('#song-list-pre-data')[0].text
		songs=json.loads(songs)
		for j in songs:
			cursor=connection.cursor()
			songname=j['name'].strip()
			if len(songname)>35:
				songname=songname[:35]
			if '"' in songname and "'" in songname:
				pass
			else:
				if '"' in songname:
					sql='insert into song(songid,albumid,songname) values(%s,%s,\'%s\')'%(j['id'],i,songname)
				else:
					sql='insert into song(songid,albumid,songname) values(%s,%s,"%s")'%(j['id'],i,songname)
			print(sql)
			cursor.execute(sql)
			cursor.close()
			connection.commit()
connection.close()

