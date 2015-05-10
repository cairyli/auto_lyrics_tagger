# auto_lyrics_tagger
 歌词搜索并嵌入mp3文件
 
1. 遍历目录下的mp3文件  
2. 通过百度搜索歌词  
3. 从虾米、百度、酷我获取歌词  
4. 把歌词嵌入mp3  
5. 把歌词写入同名txt文件  

#使用方法
放到mp3文件目录中运行  
找不到歌词的文件名会存在error.txt中  

#依赖
BeautifulSoup:用于解析HTML  
eyed3:用于读写mp3标签  
