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
	'mail_psc_fingerprint':'a1584fc59bb6a4d7e9fcf6fede4c762e',
	'_iuqxldmzr_':'32',
	'_ntes_nnid':'544a2965ba3d1d64e35494733249a7da,1550471029693',
	'_ntes_nuid':'544a2965ba3d1d64e35494733249a7da',
	'WM_TID':'3X9p%%2BMWSGz9AFBRBQRY5xO%%2F%%2FMTwsWIF7',
	'usertrack':'ezq0ZVyhVd9DxWa/FuHcAg==',
	'vinfo_n_f_l_n3':'abad5bcd59020ce9.1.0.1554542607651.0.1554542648056',
	'P_INFO':'ruchyh@163.com|1564944218|0|mail163|00&99|null&null&null#IL&null#10#0#0|156263&1||ruchyh@163.com',
	'hb_MA-9ADA-91BF1A6C9E06_source':'www.baidu.com',
	'WM_NI':'KgNjyyqFm%%2FldJiNn77VQyJj4N8t2DEvF2HRPrkIcXz18ml26JlTjk1h3J2nO3kSrTmpyfdP9LXveVmGhQCPu2T0NEPHf3Yxbimt2ujsTxe79nyuvQUMJZ4VVVVcmI9cCaGo%%3D',
	'mp_MA-9ADA-91BF1A6C9E06_hubble':'%%7B%%22sessionReferrer%%22%%3A%%20%%22https%%3A%%2F%%2Fcampus.163.com%%2Fapp%%2Fhy%%2Foverseas%%22%%2C%%22updatedTime%%22%%3A%%201571499271101%%2C%%22sessionStartTime%%22%%3A%%201571499072580%%2C%%22sendNumClass%%22%%3A%%20%%7B%%22allNum%%22%%3A%%204%%2C%%22errSendNum%%22%%3A%%200%%7D%%2C%%22deviceUdid%%22%%3A%%20%%220993f65c-4e77-440e-842e-5baeed7d8fad%%22%%2C%%22persistedTime%%22%%3A%%201571499072574%%2C%%22LASTEVENT%%22%%3A%%20%%7B%%22eventId%%22%%3A%%20%%22da_screen%%22%%2C%%22time%%22%%3A%%201571499271101%%7D%%2C%%22sessionUuid%%22%%3A%%20%%22dceb9440-cd9d-4956-93a2-a3deefd3da08%%22%%7D',
	'JSESSIONID-WYYY':'jM7quKFT6hBWKhkyv5M5pw51vdYMTvUaUWB4gf%%2FuZYIum0FkZ7nx842hfKnO3CaFKkm5oqjTJmqP9x8BK5Zx7Q6PlaJCBvDyUG0cQ6BkJgEi2tFkCw6nAYfc9xG16BIwdg8eQe26aVlAa8TwJJP2DjHHo%%2FbvQFRODl%%2BsK0rwe2WKWTfj%%3A1575979798062',
	'WM_NIKE':'9ca17ae2e6ffcda170e2e6eeacd74e92b8c0adb36b979e8aa3d14e869b8bbbf77a9ce8fad3f2808aafb9d0b12af0fea7c3b92a9bf1a1b9e55b978989b3b76e93b397bab87afcbbadb0b26e8dae8cd9fb3a8fb7beacdb44bce88191d845f19e8b83d53daebd89d5d865adb1a2d3f65a9a908885d93bf6aaffa9fb25859ba28ce148bc8eb7d2db4b95ed8687d9599bbbfa87e4258e95a8bbe16db4bcacd1db72a3b398d5ef4785af9b93c45e9389fbaed43fb4ebaeb6c837e2a3'
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
