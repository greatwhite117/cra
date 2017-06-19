# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 16:53:33 2016

@author: sspark
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def start(ctype,line, wf, logger, ing_cnt) :
    lineItem = line.split('\t')
    
    if ctype == 'api' :
        number = lineItem[0]
        keyword = lineItem[1]     
        date = lineItem[3]
        company = lineItem[9]
        title = lineItem[10]
        url_link = lineItem[12]   
    elif ctype == 'web' :
        number = lineItem[0]
        keyword = lineItem[1]     
        date = lineItem[2]
        company = lineItem[3]
        title = lineItem[4]
        url_link = lineItem[6] 
        
    session = requests.Session()
    headers = {'User-Agent':\
       'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome',\
       'Accept':\
       'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

    req = session.get(url_link, headers=headers)    
    bsobj = BeautifulSoup(req.text, 'lxml')
    logger.debug(bsobj.prettify())
    session.close()
    
    print(url_link)
    news_body = bsobj.find('div', id=has_id)
    if news_body is None :
        print('Real url : ', url_link)
        url_link = get_link(bsobj)
        if url_link == False :
            print('start_web no tag\n')
            return ing_cnt
    else :
        comments_cnt = bsobj.find('span', class_='lo_txt').string.strip()
        if comments_cnt == '0' :
            print('comments is zero...skip')
            return ing_cnt
    

    counter = ing_cnt        
    try : 
        driver = webdriver.Chrome()
        driver.implicitly_wait(1000)
        driver.get(url_link) 
        element = driver.find_element_by_css_selector('#cbox_module > div > div.u_cbox_view_comment > a > span.u_cbox_in_view_comment')
        if element is None :
            return counter
        else :
            element.click()
    except Exception as ex :
        print('collect_comments exception (1) :' + ex.message)
        logger.error('collect_comments exception (1) :' + ex.message)      
        return counter
    
    try :        
        while True :
            try :
                driver.implicitly_wait(1000)
                element = driver.find_element_by_css_selector('#cbox_module > div > div.u_cbox_paginate > a > span > span > span.u_cbox_page_more')
                if element is None :
                    break
                else :             
                    element.click()
            except Exception as ex :   
                print('exception raised = ', ex.message)
                logger.error('collect_comments Exception :' + ex.message)
                break
        
        html = driver.page_source
        bsobj = BeautifulSoup(html,'lxml')
        logger.debug(bsobj.prettify())
        cList = bsobj.find('ul',class_='u_cbox_list').find_all('li')
            

        for commentBox in cList :
            comment = commentBox.find('span', class_='u_cbox_contents').string
            cdate = commentBox.find('span', class_='u_cbox_date')['data-value']
            goodcnt = commentBox.find('em',class_='u_cbox_cnt_recomm').string
            badcnt = commentBox.find('em',class_='u_cbox_cnt_unrecomm').string                                             
            print('comments(' + str(counter) + ') ==> ' + comment + '\n')
    
            text = str(counter) + '\t' + comment + \
                 '\t' + cdate[0:19] + '\t' + goodcnt + '\t' + badcnt + \
                 '\t' + number + '\t' + keyword + '\t' + date + \
                 '\t' + company + '\t' + title + '\n'
                     
            wf.write(text)        
            counter = counter + 1
    except Exception as ex :
        print('collect_comments exception (2) :' + ex.message)
        logger.error('collect_comments exception (2) :' + ex.message)
        
    print('finish scraping....')   
    driver.quit()   
    return counter
    
def get_link(bsobj) :
    element = bsobj.find('meta', property='og:url')
    if element is None :
       return False
    else :
       url = element['content'].strip().replace('%250A','').replace('/error/unknown','read').replace('&amp;','&')
       print(url)
       return url  
       
def has_id(idName):
    if idName == 'articleBodyContents' or idName == 'articeBody':
        return True
    else:
        return False       
