# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:36:35 2016

@author: Sang
"""

from selenium import webdriver
#import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

import codecs
from bs4 import BeautifulSoup

'''''''''''''''''''''''''''''''''''
fuction section
'''''''''''''''''''''''''''''''''''
    
''' selenium naver talk scraping function '''
def scrap_web(driver, selector, file, cnt) :    
    try : 
        #print(selector)
        driver.implicitly_wait(10000)
        element = driver.find_element_by_css_selector(selector)
        element.click()
        html = driver.page_source
        
        msgList = parse_html(html)
        for msg in msgList :
            file.write(msg + '\n')
        print('*************** page size(' + str(cnt) + ') = ' + str(len(html)))
    except :
        print('scrap_web exception ==> ' + selector)
        return -1
                
    return len(html)
    
def parse_html(html) :
    msgList = []
    soupRoot = BeautifulSoup(html,'lxml') 
    msgs = soupRoot.find('div', class_='u_cbox_content_wrap').find('ul', class_='u_cbox_list').find_all('li')
    for msgObject in msgs :
        msg = msgObject.find('span', class_='u_cbox_contents').string # 댓글       
        time = msgObject.find('div', class_='u_cbox_info_base').span['data-value'] #게시일시
        #tmpStr = msg + '    ' + time
        msgList.append(msg)
    
    return msgList
    
   


'''''''''''''''''''''''''''''''''''
program start point
'''''''''''''''''''''''''''''''''''
file = codecs.open("naver_news_comments.txt", encoding="utf-8", mode="w")

driver = webdriver.Chrome()
#driver = webdriver.Ie()
#driver = webdriver.Firefox()
driver.implicitly_wait(1000)
#driver.get("http://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=102&oid=001&aid=0008510143")
driver.get("http://entertain.naver.com/read?oid=076&aid=0002953503&gid=999339&cid=1018815")

element = driver.find_element_by_css_selector('#cbox_module > div > div.u_cbox_view_comment > a > span.u_cbox_in_view_comment')
element.click()

exit_flag = False
while exit_flag == False :
    try :
        driver.implicitly_wait(1000)
        element = driver.find_element_by_css_selector('#cbox_module > div > div.u_cbox_paginate > a > span > span > span.u_cbox_page_more')
        if element is None :
             print('exit...')
             exit_flag = True
        else :             
            element.click()
    except :   
        #print('exception raised = ', e)        
        exit_flag = True
        


html = driver.page_source
bsobj = BeautifulSoup(html,'lxml')
cList = bsobj.find('ul',class_='u_cbox_list').find_all('li')


idx = 1
for commentBox in cList :
    comment = commentBox.find('span', class_='u_cbox_contents').string
    cdate = commentBox.find('span', class_='u_cbox_date')['data-value']
    goodcnt = commentBox.find('em',class_='u_cbox_cnt_recomm').string
    badcnt = commentBox.find('em',class_='u_cbox_cnt_unrecomm').string
    print('comments(' + str(idx) + ') ==> ' + comment + '\n')
    file.write('- comment : ' + comment + '\n' + '- date : ' + cdate + '\n- good : ' + goodcnt + '\n- bad : ' + badcnt + '\n')
    idx = idx + 1
    
print('finish scraping....')   
driver.quit()   
file.close()


