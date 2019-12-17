use wangyiyun;
select d.singertype,d.singername,b.songname,c.time,c.albumcomment,a.songid,a.lyric 
from lyric3 a
left join song b on a.songid=b.songid
left join album c on b.albumid=c.albumid
left join singer d on d.singerid=c.singerid
into OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Uploads\\data1.csv'  CHARACTER SET gbk
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n';


use wangyiyun;
select a.plid,b.plname,a.songid,a.songname,a.lyric,
	case when type='语种' then topic else '' end as `语种`,
    case when type='风格' then topic else '' end as `风格`,
    case when type='情感' then topic else '' end as `情感`,
    case when type='场景' then topic else '' end as `场景`,
    case when type='主题' then topic else '' end as `听众`
from plsong3 a left join playlist b on a.plid=b.plid
into OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Uploads\\playlist.csv'  CHARACTER SET gbk
FIELDS TERMINATED BY ','  
OPTIONALLY ENCLOSED BY '"'  
LINES TERMINATED BY '\n';
