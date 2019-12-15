import pymysql
from datetime import datetime 
from bs4 import BeautifulSoup
import requests
import json
import time
import random
import re

connection=pymysql.connect(host='localhost',port=3306,user='root',password='sdfzg11b',db='wangyiyun',charset='utf8')
# cookies={
# 	'mail_psc_fingerprint':'',
# 	'_iuqxldmzr_':'32',
# 	'_ntes_nnid':'',
# 	'_ntes_nuid':'',
# 	'WM_TID':'',
# 	'usertrack':'ezq0ZVyhVd9DxWa/FuHcAg==',
# 	'vinfo_n_f_l_n3':'',
# 	'P_INFO':'',
# 	'hb_MA-9ADA-91BF1A6C9E06_source':'www.baidu.com',
# 	'WM_NI':'',
# 	'mp_MA-9ADA-91BF1A6C9E06_hubble':'',
# 	'JSESSIONID-WYYY':'',
# 	'WM_NIKE':''
# }

# headers={
# 	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
# 	'Accept-Encoding':'gzip, deflate',
# 	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
# 	'Cache-Control':'max-age=0',
# 	'Host':'music.163.com',
# 	'Upgrade-Insecure-Requests':'1',
# 	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
# }
# #获取歌曲id
# playlists=[]
# cursor=connection.cursor()
# sql='select plid from playlist where plid not in (select plid from plsong)'
# cursor.execute(sql)
# connection.commit()
# pls=cursor.fetchall()
# cursor.close()
# for i in pls:
# 	playlists.append(i[0])
# # print(playlists)
# for p in playlists:
# 	url='https://music.163.com/playlist?id=%s'%p
# 	response=requests.get(url,cookies=cookies,headers=headers)
# 	html=response.text
# 	soup=BeautifulSoup(html,'lxml')
# 	items=soup.select('.f-hide')[1].select('a')
# 	for i in items:
# 		songid=str(i)[str(i).find('id=')+3:str(i).find('">')]
# 		songname=i.text
# 		if '"' in songname:
# 			songname=songname.replace('"',"'")
# 		if len(songname)>80:
# 			songname=songname[:80]
# 		sql='insert into plsong(plid,songid,songname) values(%s,%s,"%s")'%(p,songid,songname)
# 		print(sql)
# 		cursor=connection.cursor()
# 		cursor.execute(sql)
# 		cursor.close()
# 		connection.commit()

# connection.close()

cookies={
	'WM_TID':'',
	'WM_NI':'',
	'JSESSIONID-WYYY':'',
	'WM_NIKE':'',
	'__utma':'',
	'_iuqxldmzr_':'32',
	'NTES_FS':'',
	'__gads':'',
	'vjuids':'',
	'__utma':'',
	'__oc_uuid':'',
	'usertrack':'',
	'mail_psc_fingerprint':'',
	'P_INFO':'',
	'NTES_CMT_USER_INFO':'',
	'nts_mail_user':'',
	'_ga':'',
	'_ntes_nnid':'',
	'_ntes_nuid':'',
	'vinfo_n_f_l_n3':'',
	'FSTRACK':'',
	'vjlast':'',
	'__f_':''
}
headers={
	'Accept':'text/html, application/xhtml+xml, application/xml; q=0.9, */*; q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.7, ja; q=0.3',
	'Connection':'Keep-Alive',
	'Host':'music.163.com',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
}

cursor=connection.cursor()
sql='select distinct songid from plsong where lyric is null'
cursor.execute(sql)
cursor.close()
connection.commit()
ids=cursor.fetchall()
haveid=[]
for item in ids:
	haveid.append(item[0])
# print(haveid)
for i in haveid:
	print('\n')
	try:
		url='http://music.163.com/api/song/lyric?id=%s&lv=1&kv=1&tv=-1'%i
		print(url)
		response=requests.get(url,cookies=cookies,headers=headers)
		print(response)
		html=response.text
		html=json.loads(html)
		lrc=html['lrc']['lyric']
		pat=re.compile(r'\[.*\]')
		lyric=''
		lyric=re.sub(pat, "", lrc).replace('\n',';').replace(' ',',')
		cursor=connection.cursor()
		if "'" in lyric:
			lyric=lyric.replace("'","‘")
		# print(lyric)
		sql="update plsong set lyric='%s' where songid=%s"%(lyric,i)
		print(sql)
		cursor.execute(sql)
		cursor.close()
		connection.commit()
	except Exception as e:
		print('失败：'+i)
		print(html)
		if 'uncollected' in html:
			if html['uncollected']==True:
				sql="update plsong set lyric=' ' where songid=%s"%(i)
				cursor=connection.cursor()
				cursor.execute(sql)
				cursor.close()
				connection.commit()
		if 'nolyric' in html:
			if html['nolyric']==True:
				sql="update plsong set lyric=' ' where songid=%s"%(i)
				cursor=connection.cursor()
				cursor.execute(sql)
				cursor.close()
				connection.commit()

connection.close()
