# -*- coding: utf-8 -*-
"""
Created on Thu Mar 03 12:36:35 2016

@author: Sang
"""

from selenium import webdriver
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
file = codecs.open("D:\\smba2_crawler\\result\\gawang_talk.txt", encoding="utf-8", mode="w")
#file = codecs.open("D:\\smba2_crawler\\result\\samsi_talk.txt", encoding="utf-8", mode="w")
#file = codecs.open("D:\\smba2_crawler\\result\\gawang_talk.txt", encoding="utf-8", mode="w")

driver = webdriver.Chrome()
driver.implicitly_wait(1000)
driver.get("http://entertain.naver.com/tvBrand/mask")

html = driver.page_source
msgList = parse_html(html)
for msg in msgList :
    file.write(msg + '\n')
  
print('*************** page size(1) = ' + str(len(html)))

scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a:nth-child(4) > span',file,2)
scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a:nth-child(5) > span',file,3)
scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a:nth-child(6) > span',file,4)
scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a.u_cbox_page.last-child > span',file,5)

exit_flag = False

cnt = 5
while 1 == 1 :
    index = 3
    while index <= 7 :
        cnt = cnt + 1 
        if index == 3 : #다음페이지로 이동
            rtn = scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a:nth-child(8) > span.u_cbox_ico_page',file,cnt)
            if rtn < 60000 & rtn != -1 : # 더이상 없음
                exit_flag = True
                break
        elif index == 7: # 마지막페이지
            rtn = scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a.u_cbox_page.last-child > span',file,cnt)
            if rtn < 60000 & rtn != -1 :
                exit_flag = True
                break
        else :
            rtn = scrap_web(driver,'#cbox_module > div > div.u_cbox_paginate > div > a:nth-child(' + str(index) + ') > span',file,cnt)
            if rtn < 60000 & rtn != -1 :
                exit_flag = True
                break       
        index = index + 1
    if exit_flag == True :
        break
                
print('finish scraping....')      
driver.quit()
file.close()


