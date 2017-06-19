# -*- coding: utf-8 -*-
"""
Created on Wed Jul 06 15:07:48 2016

@author: sspark
"""

from __future__ import print_function
import codecs
import requests
import logging
import datetime
from urllib import quote
from bs4 import BeautifulSoup
import time

base_path = 'D:\\smba2_crawler\\'
fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
log_path = base_path + 'title' + '_' + datetime.date.today().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(level='DEBUG', format=fmt, filename=log_path, filemode='w')
logging.basicConfig
logger = logging.getLogger('naver_web_crawler')



def start(keyword,sortOption,sdate1,sdate2,edate,startPage,pageNum,counter) :
    keyword2 = keyword.decode('utf-8').encode('euc-kr')
    keyword2 = quote(keyword2)
    

    try :
        session = requests.Session()
        headers = {'User-Agent':'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)
                                 AppleWebKit 537.36 (KHTML, like Gecko) Chrome''',
                   'Accept':'''text/html,application/xhtml+xml,application/xml;
                             q=0.9,image/webp,*/*;q=0.8'''}
        url = 'http://news.naver.com/main/search/search.nhn?' + \
              'query=' + keyword2 + '&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&' +\
              'sm=all.basic&ic=all&so=' + sortOption + '&' + \
              'stDate=range:' + sdate1 + ':' + edate + '&' + \
              'detail=0&pd=4&' + \
              'r_cluster2_start=' + str(startPage) + '&r_cluster2_display=' + '10' + '&' + \
              'start=' + str(startPage) + '&display=5&startDate=' + sdate2 + '&endDate=' + edate + '&' + \
              'page=' + str(pageNum)
                         

        logger.debug(url)
        print(url)
        req = session.get(url, headers=headers)    
        bsobj = BeautifulSoup(req.text, 'lxml')
        logger.debug(bsobj.prettify())
        session.close()

#        rf = codecs.open('D:\\smba2_crawler\\naver.html', encoding='utf-8', mode='r') 
#        text = rf.read()   
#        bsobj = BeautifulSoup(text,'lxml')
        
        
        totalInfo = get_totalInfo(bsobj)  
        if totalInfo == False :
            return 0
        print('page information :', totalInfo)
        
        newsList = get_items(bsobj,logger) 
        if newsList == False :
            return 0
        
        ing_cnt = counter
        for news in newsList :
            text =  str(ing_cnt) + '\t' + keyword.decode('utf-8') + '\t' + news[0] + '\t' + news[1] + '\t' + \
                   '\t' + news[2] + '\t' + news[3] + '\t' + news[4] +  '\n'
            wf.write(text) 
            print('news writing...', ing_cnt)
            ing_cnt = ing_cnt + 1
            
#        rf.close()       
        return ing_cnt
    
    except Exception as ex:
        print('start Exception ...==>', ex)

def get_totalCnt(bsobj) :
    element = bsobj.find('span', class_='result_num').string
    strList1 = element.split('/')
    strList2 = strList1[1].split('건'.decode('utf-8'))
    strTemp = strList2[0].replace(',','').strip()
    return strTemp
    
def get_totalInfo(bsobj) :
    element = bsobj.find('span', class_='result_num')
    if element is None :
        print('get_totalInfo...flase return\n')
        return False
    else :
        element = element.string.strip().replace('/r','').replace('\n','')
        return element    
    
        
def get_items(bsobj,logger) :    
    items = bsobj.find('div', class_='srch_result_area').find_all('ul')
    if items is None :
        print('get_items...flase return\n')
        return False
    else :
        print('parsing news...')
    newsList = []
    for item in items :
        
        title = item.find('div',class_='ct')
        if title is None :
            continue
        title = title.find('a',class_='tit').text        
        title = title.strip().replace('  ','').strip().replace("'",'')
        title = title.replace('\r','').replace('\n','').strip()
        logger.debug(title)
        
        press = item.find('div',class_='info').find('span',class_='press').string.strip()
        logger.debug(press)
        
        pubDate = get_date(item.find('div',class_='info').find('span',class_='time').string.strip())
        logger.debug(pubDate)
        
        element = item.find('a',class_='go_naver')
        if not element is None :
            naver_link = element['href'].strip()
            logger.debug(naver_link)
        else :
            naver_link = ' '
        
        element = item.find('p',class_='dsc')
        if not element is None :
            desc = element.text        
            desc = desc.strip().replace('  ','').strip().replace("'",'')
            desc = desc.replace('\r','').replace('\n','').strip()
            logger.debug(desc)
        else :
            continue  
        
        newsList.append([pubDate,press,title,desc,naver_link])
        #print('news.... ' + str(counter))       
    return newsList
        
def get_date(date) :
    if date[-2:] == '일전'.decode('utf-8') :
        today = datetime.date.today()
        diff = datetime.timedelta(int(date[0]),0,0)             
        pdate = today - diff        
        return pdate.isoformat()        
    elif date.find('.') > 0 :
        pdate = datetime.date(int(date[0:4]),int(date[5:7]),int(date[8:10]))
        return pdate.isoformat()
    else :
        return datetime.date.today().isoformat()

        
def get_newsCnt(keyword,sdate1,edate,sdate2) :
    keyword2 = keyword.decode('utf-8').encode('euc-kr')
    keyword2 = quote(keyword2)
    
    try :
        session = requests.Session()
        headers = {'User-Agent':'''Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)
                                 AppleWebKit 537.36 (KHTML, like Gecko) Chrome''',
                   'Accept':'''text/html,application/xhtml+xml,application/xml;
                             q=0.9,image/webp,*/*;q=0.8'''}
        url = 'http://news.naver.com/main/search/search.nhn?' + \
              'query=' + keyword2 + '&st=news.all&q_enc=EUC-KR&r_enc=UTF-8&r_format=xml&rp=none&' +\
              'sm=all.basic&ic=all&so=rel.dcs&' + \
              'stDate=range:' + sdate1 + ':' + edate + '&' + \
              'detail=0&pd=4&' + \
              'r_cluster2_start=1&r_cluster2_display=10&' + \
              'start=1&display=5&startDate=' + sdate2 + '&endDate=' + edate + '&' + \
              'page=1'
                         

        print(url)
        req = session.get(url, headers=headers)    
        bsobj = BeautifulSoup(req.text, 'lxml')
        session.close()        
        
        totalCnt = get_totalCnt(bsobj)        
        print(totalCnt)
        return totalCnt   

    
    except Exception as ex:
        print('get_newsCnt Exception....==>', ex)  
        
def get_startPage(i) :
    if i == 10 or i == 100 or i == 1000 or i == 10000 or \
       i == 100000 or i == 1000000 :
        i = i - 1
        
    strI = str(i)
    len_cnt = len(strI)
    
    if len_cnt == 1 :
        startPage = '1'
    else :
        offset = len_cnt - 1
        startPage = strI[0:offset] + '01'
          
    return startPage
 
   
##############################################################################    
keyword = '함부로 애틋하게'
sortOption = 'rel.dsc' # 관련도순 : rel.dsc / 최신순 : datetime.dsc
sdate1 = '20160708'
sdate2 = '2016-07-08'
edate = '20160708'
newscnt = 20  # 0 : 기간내 전체 수집

if newscnt == 0 : # 기간내 전체 수집
   newscnt = int(get_newsCnt(keyword,sdate1,edate,sdate2))
   print('total news cnt : ', newscnt)

modVal = newscnt % 10
if modVal == 0 :
    loop_count = newscnt / 10
else :
    loop_count = newscnt / 10 + 1  

wf = codecs.open('D:\\smba2_crawler\\naver_news.txt', encoding='utf-8', mode='w')
i = 1
counter = 1
while  i <= loop_count : 
    pageNum = i
    startPage = get_startPage(i)
    
    print('page Number : ', pageNum, 'start page : ', startPage)  
    time.sleep(5)
    counter = start(keyword,sortOption,sdate1,sdate2,edate,startPage,pageNum,counter)
    if counter == 0 :
        break
    i = i + 1

print('#####################################')    
print('program is finished')    
wf.close()    
                  
    








