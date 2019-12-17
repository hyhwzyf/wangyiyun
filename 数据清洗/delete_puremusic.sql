--删除主体数据中纯音乐（分别删除95130，2926，594，2413首歌曲）
use wangyiyun
SET SQL_SAFE_UPDATES=0
delete from lyric where lyric=' '
delete from lyric where lyric like '%纯音乐%'
delete from lyric where lyric like '%暂无歌词%'
delete FROM lyric where CHAR_LENGTH(lyric)<40;

--删除歌单数据中纯音乐（分别删除42675，717，5，720首歌曲）
delete from plsong where lyric=''
delete from plsong where lyric like '%纯音乐%'
delete from plsong where lyric like '%%暂无歌词%%'
delete FROM plsong where CHAR_LENGTH(lyric)<40
