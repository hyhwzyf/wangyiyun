use wangyiyun;
select b.songname,c.time,c.albumcomment,a.songid,a.lyric from lyric3 a 
left join song b on a.songid=b.songid
left join album c on b.albumid=c.albumid
into OUTFILE 'C:\\ProgramData\\MySQL\\MySQL Server 5.7\\Uploads\\data1.csv'  CHARACTER SET gbk
 FIELDS TERMINATED BY ','  
 OPTIONALLY ENCLOSED BY '"'  
 LINES TERMINATED BY '\n';

