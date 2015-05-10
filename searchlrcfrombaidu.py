#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urllib2
import urllib
from bs4 import BeautifulSoup
import re

useragent='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36 OPR/29.0.1795.47'
def getLrcFromKuwo(link):
    '''从酷我解析歌词'''
    lyrics_html = urllib2.urlopen(link).read()
    soup = BeautifulSoup(lyrics_html)
    raw_lyrics= (soup.findAll('div', attrs={'id' : 'lrcContent'}))
    paras=[]
    test1=unicode.join(u'\n',map(unicode,raw_lyrics))

    #test1= (test1.replace('<div id="lrcContent">','\n'))
    test1=re.sub('<div id="lrcContent">[\s]*','',test1)
    test1= (test1.replace('<br/>',''))
    test1= (test1.replace('</br>',''))
    test1= (test1.replace('<br>','\n'))
    test1 = test1.replace('</p>',' ') 
    test1 = test1.replace('</div>','') 
    test1=test1.strip()
    return test1

def getLrcFromXiami(link):
    '''从虾米解析歌词'''
    request = urllib2.Request(link)
    request.add_header('User-Agent',useragent)
    lyrics_html = urllib2.urlopen(request).read()
    soup = BeautifulSoup(lyrics_html)
    raw_lyrics= (soup.findAll('div', attrs={'class' : 'lrc_main'}))
    paras=[]
    test1=unicode.join(u'\n',map(unicode,raw_lyrics))

    #test1= (test1.replace('<div id="lrcContent">','\n'))
    test1=re.sub('<div class="lrc_main">[\s]*','',test1)
    test1= (test1.replace('<br/>',''))
    test1= (test1.replace('</br>',''))
    test1= (test1.replace('<br>','\n'))
    test1 = test1.replace('</p>',' ') 
    test1 = test1.replace('</div>','') 
    test1=test1.strip()
    return test1

def getLrcFromBaidu(link):
    '''从百度音乐解析歌词'''
    request = urllib2.Request(link)
    request.add_header('User-Agent',useragent)
    lyrics_html = urllib2.urlopen(request).read()
    soup = BeautifulSoup(lyrics_html)
    divs_lyrics= (soup.findAll('div', attrs={'id' : 'lyricCont'}))
    test1=''
    if divs_lyrics:
        link_lyrics='http://music.baidu.com'+divs_lyrics[0].attrs['data-lrclink']
        request = urllib2.Request(link_lyrics)
        request.add_header('User-Agent',useragent)
        raw_lyrics = urllib2.urlopen(request).read()  
    #paras=[]
    #test1=unicode.join(u'\n',map(unicode,raw_lyrics))
    #test1= (test1.replace('<div id="lrcContent">','\n'))
        test1=re.sub('\[[^\]]+\]','',raw_lyrics)
        test1= (test1.replace('<br/>',''))
        test1= (test1.replace('</br>',''))
        test1= (test1.replace('<br>','\n'))
        test1 = test1.replace('</p>',' ') 
        test1 = test1.replace('</div>','') 
        test1=test1.strip()
    return test1

def searchLrcFromBaidu(name):
    #name=name.decode('utf-8')
    urltemplate = 'http://www.baidu.com/s?wd='+urllib.quote(name)+'&pn='
    #url=urllib.quote(url)
        #url = 'http://cn.bing.com/search?q=site:www.metrolyrics.com '+name
    for pn in ('0','10','20'):
        req = urllib2.Request(urltemplate+pn, headers={'User-Agent' : useragent})
        response = urllib2.urlopen(req)
        result = response.read()
        #str = unicode(str, errors='replace')
        ##print(str.encode('utf8'))
        #result = str.encode('utf8') 
        link_start=-1
        lrc=''
        link_sources={
            'www.xiami.com/lrc':getLrcFromXiami,
            'www.xiami.com/song':getLrcFromXiami,
            'music.baidu.com/song':getLrcFromBaidu,
            'www.kuwo.cn/yinyue':getLrcFromKuwo
        }
        for i in link_sources:
            link_start=result.find(i)
            if link_start>=0:
                m=re.search('"url":"([^"]+)"', result[link_start:], flags=0)
                if m:
                    link=m.group(1)
                    if link:
                        try:
                            lrc=link_sources[i](link)
                        except urllib2.HTTPError:
                            continue
                        if lrc:
                            return lrc
                    
    #link_end=result.find('html',link_start+1)
    #print(result[link_start:link_start+57])
    return lrc
if __name__=='__main__':
    #getLrcFromKuwo('http://www.kuwo.cn/yinyue/6368377')
    test1=searchLrcFromBaidu('G.E.M.邓紫棋 - 单行的轨道 歌词')
    #link='http://music.baidu.com/song/239779239?fm=altg5'
    #if link:
        #getLrcFromBaidu(link)