# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 10:36:14 2016

@author: sspark
"""
from __future__ import print_function
import requests
from bs4 import BeautifulSoup
import datetime
import time

########################
def start(api_type,api_id,api_secret,crl_keyword,crl_cnt,wf,list_path,logger, ing_cnt) :
    
    if crl_cnt == 0 : ## 전체 건수 수집이라면
        crl_cnt = get_total_cnt(api_type,api_id,api_secret,crl_keyword,logger)
        
    if crl_cnt == -1 :
        return -1

    if crl_cnt <= 100 :
        one_cnt = crl_cnt
    else :
        one_cnt = 100
    
    modVal = crl_cnt % one_cnt
    if modVal == 0 :
        loop_count = crl_cnt / one_cnt
    else :
        loop_count = crl_cnt / one_cnt + 1
    
    i = 0
    counter = ing_cnt
    while  i < loop_count : 
        startIdx = i * one_cnt + 1
        
        if i == (loop_count - 1) and modVal <> 0 : #마지막인 경우
            one_cnt = modVal
            
        counter = call_api(api_type,api_id,api_secret,crl_keyword,
                 str(one_cnt),str(startIdx),wf,logger,counter)
        i = i + 1
          
    return counter

########################    
def call_api(api_type,api_id,api_secret,crl_keyword,
             one_cnt, startIdx,wf,logger,counter) :
    try :
        session = requests.Session()
        headers = {'User-Agent':'curl/7.43.0', 'Accept':'*/*', 
                   'Content-type':'application/xml',
                   'X-Naver-Client-Id':api_id, 
                   'X-Naver-Client-Secret':api_secret}
                   
        url = 'https://openapi.naver.com/v1/search/' + api_type + '.xml?query=' + \
              crl_keyword + '&display=' + one_cnt + '&start=' + startIdx + '&sort=sim'
              
        req = session.get(url, headers=headers)
        bsobj = BeautifulSoup(req.text,'xml')
        logger.debug(bsobj.prettify())
        
        if not bsobj.find('errorMessage') is None :
            errMsg = bsobj.find('errorMessage').string
            print('naver api 에러 : ', errMsg, crl_keyword, one_cnt, startIdx)     
            return counter
        
        items = bsobj.find_all('item')
        
        for item in items :
            write_file(api_type, crl_keyword, item, wf,logger,counter)
            counter = counter + 1
        session.close() 

        
    except Exception as ex:
        print('collect_naver - call_api Exception :', ex.message)
        logger.error('collect_naver - call_api :' + ex.message)
        return counter
        
    return counter
    
########################       
def write_file(api_type, crl_keyword, item, wf, logger, idx) :
    title = item.title.get_text().replace('<b>',' ').replace('</b>',' ')\
            .replace('&lt;', '<').replace('&gt;','>').replace('&quot;','"')    
            
    desc = item.description.get_text().replace('<b>',' ').replace('</b>',' ')\
            .replace('&lt;', '<').replace('&gt;','>').replace('&quot;','"') 
            
    link = str(item)       
    s_idx = link.find('http://openapi')
    e_idx = link.find('</link>')
    
    link = link[s_idx:e_idx]
    
    if api_type == 'news' : 
       time.sleep(0.5)
       comments_cnt, like_cnt, company = get_info(link,logger)      
       #comments_cnt, like_cnt, company = ('0','0','N/A') 
       pubDate = item.pubDate.get_text()
       date = datetime.datetime(int(pubDate[12:16]),int(set_month(pubDate[8:11])),\
              int(pubDate[5:7]),int(pubDate[17:19]),int(pubDate[20:22]),int(pubDate[23:25]))
       text = str(idx) + '\t' + crl_keyword + '\t' + api_type + '\t' + date.strftime('%Y-%m-%d') + \
             '\t' + date.strftime('%H') + '\t' + date.strftime('%M') + '\t' + date.strftime('%A') + \
             '\t' + comments_cnt + '\t' + like_cnt + '\t' + company + \
             '\t' + title + '\t' + desc + '\t' + link + '\n'
    else :
       text = str(idx) + '\t' + crl_keyword + '\t' + api_type + '\t' + ' ' + \
             '\t' + ' ' + '\t' + ' ' + '\t' + ' ' + \
             '\t' + ' ' + '\t' + ' ' + '\t' + ' ' + \
             '\t' + title + '\t' + desc + '\t' + link + '\n'
             
    wf.write(text)
    print('items collecting....' + str(idx))
    logger.debug(text)
                         
########################  
def get_info(url,logger) :
    session = requests.Session()
    headers = {'User-Agent':\
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome',\
               'Accept':\
               'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    try :           
        req = session.get(url, headers=headers)    
        bsObj = BeautifulSoup(req.text, 'lxml')
        session.close()  
                 
        try :
            comments_cnt = bsObj.find('span', class_='lo_txt').string
            like_cnt = bsObj.find('div', class_='u_likeit_module').find('a').get_text()        
            company = bsObj.find('div', class_='press_logo').find('img')['title']       
            return (comments_cnt, like_cnt, company)
            
        except :
            try :                
                comments_cnt = bsObj.find('a', class_='reply_count').string
                company = bsObj.find('div', class_='press_logo').find('img')['alt']
                if comments_cnt is None :
                    comments_cnt = '0'
                return(comments_cnt, '0', company)
            except :
                #print('collect_naver - get_info Exception :', ex.message, url)
                #logger.error('collect_naver - get_info Exception : ' + ex.message + url)
                return ('0', '0', 'N/A')
    except Exception as ex :
        print('collect_naver-get_info exception :' + ex.message)
        logger.error('collect_naver-get_info exception :' + ex.message)
        return ('0', '0', 'N/A')
                                
                         
########################     
def get_total_cnt (api_type,api_id,api_secret,crl_keyword,logger) :
    
    try :
        session = requests.Session()
        headers = {'User-Agent':'curl/7.43.0', 'Accept':'*/*', 
                   'Content-type':'application/xml',
                   'X-Naver-Client-Id':api_id, 
                   'X-Naver-Client-Secret':api_secret}
                   
        url = 'https://openapi.naver.com/v1/search/' + api_type + '.xml?query=' + \
              crl_keyword + '&display=1&start=1&sort=sim'
              
        req = session.get(url, headers=headers)
        bsobj = BeautifulSoup(req.text,'xml')
        total_cnt = bsobj.find('total').get_text()
        logger.warn(total_cnt)
        
        session.close() 
        return int(total_cnt)
        
    except Exception as ex:
        print('collect_naver - get_total_cnt Exception :' + ex.message)
        logger.error('collect_naver - get_total_cnt Exception : ' + ex.message)
        return -1
        
def set_month(mm) :
    if mm == 'Jan' :
        return '01'
    elif mm == 'Feb' :
        return '02'
    elif mm == 'Mar' :
        return '03'
    elif mm == 'Apr' :
        return '04'        
    elif mm == 'May' :
        return '05'        
    elif mm == 'Jun' :
        return '06'
    elif mm == 'Jul' :
        return '07'
    elif mm == 'Aug' :
        return '08'
    elif mm == 'Sep' :
        return '09'
    elif mm == 'Oct' :
        return '10'        
    elif mm == 'Nov' :
        return '11'        
    elif mm == 'Dec' :
        return '12'         