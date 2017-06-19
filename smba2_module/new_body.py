    # -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 16:12:37 2016

@author: sspark
"""
from __future__ import print_function
import requests
import codecs
from bs4 import BeautifulSoup



base_path = 'C:\\smba2_crawler\\result_web\\'
list_path = base_path + '가짜뉴스' + '_list.txt'  #뉴스, 블로그, 카페 통합 리스트
newsbody_path = base_path + '가짜뉴스' + '_newsBody.txt' # 뉴스 원문


print('Collecting Naver News Body is Started ..... \n')
wf = codecs.open(newsbody_path,encoding='utf-8',mode='w')
rf = codecs.open(list_path,encoding='utf-8',mode='r')
       
for line in rf.readlines() :
    lineItem = line.split('\t')
    time.sleep(1)
    if not lineItem[6] is None and len(lineItem[6]) > 10 :
        start_web(line, wf, logger)
     
rf.close()          
wf.close()
print('Collecting Naver News Body is Finished ..... \n')




def start(line, wf, logger) :
    lineItem = line.split('\t')
    number = lineItem[0]
    keyword = lineItem[1]     
    date = lineItem[3]
    company = lineItem[9]
    title = lineItem[10]
    desc = lineItem[11]
    url_link = lineItem[12]
    
    session = requests.Session()
    headers = {"User-Agent" : "Mozilla/5.0", "referer" : "http://m.naver.com"}


    try :
        req = session.get(url_link, headers=headers)    
        bsobj = BeautifulSoup(req.text, 'lxml')
        logger.debug(bsobj.prettify())
        session.close()    
        
        news_body = bsobj.find('div', id=has_id)
        if news_body is None :
            print('news_body is None\n')
            return False                   
        logger.debug(url_link + 'news body writing...' + number)
        
        wf.write('\n- number      : ' + number + '\n')
        wf.write('- pubDate     : ' + date + '\n')        
        wf.write('- keyword     : ' + keyword + '\n')        
        wf.write('- press corp. : ' + company + '\n') 
        wf.write('- news link   : ' + url_link + '\n')         
        wf.write('- title       : ' + title + '\n')
        wf.write('- description : ' + desc + '\n')       
        wf.write('- body        :\n')
        wf.write(news_body.get_text().strip().replace('  ','').replace('\r','').replace('\n','').strip())
    
    except :
        print('no naver news', url_link)
        logger.debug('no naver news' + url_link)
        return False
        


def start_web(line, wf, logger) :
    lineItem = line.split('\t')
    number = lineItem[0]
    keyword = lineItem[1]     
    date = lineItem[2]
    company = lineItem[3]
    title = lineItem[4]
    desc = lineItem[5]
    url_link = lineItem[6]
    
    print(url_link)
    if len(url_link) < 5:
        return False    
    
    session = requests.Session()
    headers = {"User-Agent" : "Mozilla/5.0", "referer" : "http://m.naver.com"}



    try :
        req = session.get(url_link, headers=headers)    
        bsobj = BeautifulSoup(req.text, 'lxml')
        logger.warn(bsobj.prettify())
        session.close()    
        news_body = bsobj.find('div', id=has_id)
        if news_body is None :
            url = get_link(bsobj)
            if url == False :
                print('start_web no tag\n')
                return False
            else :
                print('Real url :', url)
                if call_page(line,url,wf,logger) == False :
                    return False
                else : 
                    return True
            
        logger.debug(url_link + 'news body writing...' + number)
        
#        wf.write('\n- number      : ' + number + '\n')
#        wf.write('- pubDate     : ' + date + '\n')        
#        wf.write('- keyword     : ' + keyword + '\n')        
#        wf.write('- press corp. : ' + company + '\n') 
#        wf.write('- news link   : ' + url_link + '\n')         
        wf.write('- title       : ' + title + '\n')
#        wf.write('- description : ' + desc + '\n')       
        wf.write('- body        :\n')
        wf.write(news_body.get_text().strip().replace('  ','').replace('\r','').replace('\n','').strip())
    
    except :
        print('no naver news', url_link)
        logger.debug('no naver news' + url_link)
        return False  
        
def call_page(line,url_link,wf,logger) : 
    lineItem = line.split('\t')
    number = lineItem[0]
    keyword = lineItem[1]     
    date = lineItem[2]
    company = lineItem[3]
    title = lineItem[4]
    desc = lineItem[5]
    
    session = requests.Session()
    headers = {"User-Agent" : "Mozilla/5.0", "referer" : "http://m.naver.com"}
    try :
        req = session.get(url_link, headers=headers)    
        bsobj = BeautifulSoup(req.text, 'lxml')
        logger.warn(bsobj.prettify())
        session.close()    
        
        news_body = bsobj.find('div', id=has_id)
        if news_body is None :
            return False                
            
        logger.debug(url_link + 'news body writing...' + number)
        
        wf.write('- number      : ' + number + '\n')
        wf.write('- pubDate     : ' + date + '\n')        
        wf.write('- keyword     : ' + keyword + '\n')        
        wf.write('- press corp. : ' + company + '\n') 
        wf.write('- news link   : ' + url_link + '\n')         
        wf.write('- title       : ' + title + '\n')
        wf.write('- description : ' + desc + '\n')       
        wf.write('- body        :\n')
        wf.write(news_body.get_text().strip().replace('  ','').replace('\r','').replace('\n','').strip())
        
        return True
    
    except :
        print('no naver news', url_link)
        logger.debug('no naver news' + url_link)
        return False    
        
        
def has_id(idName):
    if idName == 'articleBodyContents' or idName == 'articeBody':
        return True
    else:
        return False
        
def get_link(bsobj) :
    element = bsobj.find('meta', property='og:url')
    if element is None :
       return False
    else :
       url = element['content'].strip().replace('%250A','').replace('/error/unknown','read').replace('&amp;','&')
       print(url)
       return url