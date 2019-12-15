import pymysql
from datetime import datetime 
from bs4 import BeautifulSoup
import requests
import json
import time
import random
import re
# import urllib.parse
# import base64
# from Crypto.Cipher import AES
# from binascii import hexlify


#grab lyrics
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
# headers={
# 	'origin':'https://music.163.com',
# 	'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
# 	'content-type':'application/x-www-form-urlencoded',
# 	'accept-encoding':'gzip, deflate, br',
# 	'accept-language':'zh-CN,zh;q=0.9,en;q=0.8',
# 	'content-length':'390'
# }
# data={
# 	'params':'8LDlXf9miYmH1UEYKmJpWhi39vg+9NIDXAhPw1yeLm2kMGoIWY8pUl5tvElbiN0fv9+mRmhqxSF6trlb6xYnBjbzig9HRdXZ5MqSuFTVF6Q=',
# 	'encSecKey':'8461758f4ff063c613214a6a86442536ada6d167c12dfff9e923f5e74fc85cf26fdd6846399eb23dbf3364e3d1b8f4e05525bc7198a68d90a65b480e78eb0fd85873e17badc08fd6dc1b86758eb8398a3baeb5d30fe48115aeca3039871e52b38cd28407a3e4d6a8fbb6ca88c5e47d4d23b738bd34b548b8052de7c156b92d3c'
# }

headers={
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate',
	'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
	'Cache-Control':'max-age=0',
	'Host':'music.163.com',
	'Upgrade-Insecure-Requests':'1',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

connection=pymysql.connect(host='localhost',port=3306,user='root',password='11111111',db='wangyiyun',charset='utf8')
cursor=connection.cursor()
sql='select distinct songid from song where songid not in (select songid from lyric)'
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
		response=requests.post(url,cookies=cookies,headers=headers)
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
		print(lyric)
		sql="insert into lyric(songid,lyric) values(%s,'%s')"%(i,lyric)
		cursor.execute(sql)
		cursor.close()
		connection.commit()
	except Exception as e:
		print('失败：'+i)
		print(html)
		if 'uncollected' in html:
			if html['uncollected']==True:
				sql="insert into lyric(songid,lyric) values(%s,' ')"%(i)
				cursor=connection.cursor()
				cursor.execute(sql)
				cursor.close()
				connection.commit()
		if 'nolyric' in html:
			if html['nolyric']==True:
				sql="insert into lyric(songid,lyric) values(%s,' ')"%(i)
				cursor=connection.cursor()
				cursor.execute(sql)
				cursor.close()
				connection.commit()

connection.close()

# 395995  100111



# def get_random_str():
# 	str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
# 	random_str = '';
# 	for i in range(16):
# 		index = random.randint(0,len(str)-1);
# 		random_str += str[index];
# 	return random_str;

# def aes_encrypt(text,key):#text是要加密的密文，key是密钥
# 	iv = b'0102030405060708';
# 	pad = 16 - len(text) % 16;
# 	text = text + chr(2) * pad;
# 	encryptor = AES.new(key.encode(),AES.MODE_CBC,iv);
# 	encryptor_str = encryptor.encrypt(text.encode());
# 	result_str = base64.b64encode(encryptor_str).decode();
# 	return result_str;

# def rsa_encrypt(text):#text是16位的随机字符串
# 	pub_key = '010001';#js中的e
# 	# js中的f
# 	modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
# 	text = text[::-1];
# 	result = pow(int(hexlify(text.encode()),16),int(pub_key,16),int(modulus,16));
# 	return format(result,'x').zfill(131);

# #b函数，两次AES加密
# def get_aes(text,random_str):
# 	first_aes = aes_encrypt(text,key='0CoJUm6Qyw8W8jud');#key是固定的，相当于g
# 	second_aes = aes_encrypt(first_aes,random_str);
# 	return second_aes;

# #获取加密的参数
# def get_post_data(text,random_str):
# 	params = get_aes(text,random_str);
# 	encSecKey = rsa_encrypt(random_str);
# 	return {'params':params,'encSecKey':encSecKey};


# def get_song_list(song_name,random_str):
# 	#要加密的字符串
# 	text = {"hlpretag":"<span class=s-fc7>","hlposttag":"</span>","s":song_name,"type":"1","offset":"0","total":"true","limit":"50","csrf_token":""};
# 	text = json.dumps(text);
# 	data = get_post_data(text,random_str);
# 	url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=';
# 	return post_requests(url,data);

# def post_requests(url,data):
# 	session = requests.Session();
# 	session.headers.update(headers);
# 	re = session.post(url,data=data);
# 	return re.json();


# def get_song_url(song_id,random_str):
# 	#'MD 128k': 128000, 'HD 320k': 320000
# 	text = {'ids': [song_id], 'br': 128000, 'csrf_token': ''};
# 	text = json.dumps(text);
# 	data = get_post_data(text,random_str);
# 	url = 'https://music.163.com/weapi/song/enhance/player/url?csrf_token=';
# 	return post_requests(url,data);

# random_str = get_random_str()
# data=get_post_data("{'ids':327429,'br':128000,csrf_token':''}",random_str)
# print(data)
# if __name__ == '__main__':
# 	random_str = get_random_str();
# 	song_name = input('输入歌曲名：')
# 	song_list = get_song_list(song_name,random_str);
# 	id = song_list['result']['songs'][0]['id'];
# 	song_url = get_song_url(id,random_str)['data'][0]['url'];
# 	if not os.path.exists(song_name):
# 		os.mkdir(song_name);#新建文件夹
# 	with open(song_name+'/'+song_name+'.mp3','wb') as f:
# 		try:
# 			response = requests.get(song_url, timeout=10);
# 		except requests.exceptions.ConnectTimeout:#超时重新请求
# 			response = requests.get(song_url, timeout=10);
# 		f.write(response.content);
