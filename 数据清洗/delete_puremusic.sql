--删除纯音乐（删除约9.5万首歌曲）
use wangyiyun
SET SQL_SAFE_UPDATES=0
delete from lyric where lyric=' '
delete from lyric where lyric like '%纯音乐%'
delete from lyric where lyric like '%暂无歌词%'
