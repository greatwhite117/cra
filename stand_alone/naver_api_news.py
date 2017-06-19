# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 11:17:48 2016

@author: sspark
"""

from __future__ import print_function
import codecs
import requests
import math
from bs4 import BeautifulSoup

###################################################
"""
function section 
"""

def get_newsbody(item):
    item = str(item)
        
    s_idx = item.find('http://openapi')
    e_idx = item.find('</link>')
    
    linkUrl = item[s_idx:e_idx]     
    #print(linkUrl)
    
    return get_content(linkUrl)
    
def get_content(url):
    session = requests.Session()
    headers = {'User-Agent':'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)
                             AppleWebKit 537.36 (KHTML, like Gecko) Chrome''',
               'Accept':'''text/html,application/xhtml+xml,application/xml;
                         q=0.9,image/webp,*/*;q=0.8'''}
    try :
        req = session.get(url, headers=headers)    
        bsObj = BeautifulSoup(req.text, 'lxml')
        #print(bsObj.prettify())
        session.close()
        news_body = bsObj.find('div', id=has_id)
    except :
        print('news content crawling failed...skip')
        news_body = None

    if news_body is None : #news_body가 없을 경우 None Type 리턴        
        return 'skip'
    else :
        return news_body.get_text().strip() # 태그안에 있는 모든 텍스트 리턴
        
        
def has_id(idName):
    if idName == 'articleBodyContents' or idName == 'articeBody':
        return True
    else:
        return False
    
    
        
def start_crawling(keyword,displayCnt,startIdx) :
    session = requests.Session()
    headers = {'User-Agent':'curl/7.43.0', 'Accept':'*/*', 
               'Content-type':'application/xml',
               'X-Naver-Client-Id':'qIDwAwAuX7L9EwgEEz2B', 
               'X-Naver-Client-Secret':'J1ydQKyp8V'}
               
    url = 'https://openapi.naver.com/v1/search/news.xml?query=' + keyword + '&display=' + displayCnt + '&start=' + startIdx + '&sort=sim'
    req = session.get(url, headers=headers)
    session.close()
    
    bsobj = BeautifulSoup(req.text,'xml')
    #print(bsobj.prettify())
    
    items = bsobj.find_all('item') ## 뉴스 아이템
    

    
    for item in items :
        news_title = item.title.get_text().replace('<b>',' ').replace('</b>',' ').replace('&lt;', '<').replace('&gt;','>').replace('&quot;','"')    
        news_pubDate = item.pubDate.get_text()
        news_content = get_newsbody(item)    
        if news_content != 'skip' :
            print('writing news (Naver News) ==> ' + news_title +  '\n')
            wf.write('- title        : ' + news_title + '\n')        
            wf.write('- publish Date : ' + news_pubDate + '\n') 
            wf.write('- news content : \n')           
            wf.write(news_content + '\n\n')
        else :
            print('skip news (Original News) ===> ' + news_title + '\n')
        
 

###################################################



###################################################        
    
"""
 program start point 
 
"""
keyword = '브렉시트' # 뉴스 키워드
one_count = 10  # API 1회 호출시 가져올 뉴스 건수
all_count = 10 # 전체 가져올 뉴스 건수

loop_count = math.ceil(all_count / one_count)
i = 0

## 파일 저장
wf=codecs.open('naver_news.txt',encoding='utf-8',mode='w')
    
while  i < loop_count : 
    startIdx = i * one_count + 1
    start_crawling(keyword,str(one_count),str(startIdx))
    i = i + 1
    
wf.close()  

################################################### 