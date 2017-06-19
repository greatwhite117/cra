#-*- coding: utf-8 -*-

"""
Created on Tue Jul 05 09:44:42 2016

@author: sspark
"""

import sys
import logging
import codecs
from smba2_module import collect_web_news, collect_news_body, collect_comments, hangul_mining
import datetime
import time



## step1. 저장할 파일 지정


base_path = 'C:\\smba2_crawler\\new\\'
list_path = base_path + 'ne_review' + '_list.txt'  #뉴스, 블로그, 카페 통합 리스트

listNoun_path = base_path + 'ne_review' + '_listNoun.txt' # 리스트 명사 분석
listPhrase_path = base_path + 'ne_review' + '_listPhrase.txt' # 리스트 의미단위 분석
listTagging_path = base_path + 'ne_review' + '_listTagging.txt' # 리스트 품사태깅 분석

## step2. 로깅 파일 설정
fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
log_path = base_path +'ne_review' + '_' + datetime.date.today().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(level='WARN', format='fmt', filename='log_path', filemode='w')
logging.basicConfig
logger = logging.getLogger('naver_web_crawler')


#############################################################################   
## step6. 리스트 키워드 분석   
print('Analyzing List Items is Started ..... \n')
wf = codecs.open(listNoun_path,encoding='utf-8',mode='w')
rf = codecs.open(list_path,encoding='utf-8',mode='r')

lineList = []
for line in rf.readlines() :
    lineItem = line.split('\t')
    review = lineItem[0]
    lineList.append(review)
    
## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
hangul_mining.start('noun', lineList, wf, logger)

rf.close()
wf.close()
print('Analyzing List Items is Finished ..... \n')   

print('Analyzing List Items is Started ..... \n')

wf = codecs.open(listPhrase_path,encoding='utf-8',mode='w')
rf = codecs.open(list_path,encoding='utf-8',mode='r')

lineList = []
for line in rf.readlines() :
    lineItem = line.split('\t')
    review = lineItem[0]    
    scorre = lineItem[1]    
    lineList.append(review + ' ' + score)
#    
## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
hangul_mining.start('phrase', lineList, wf, logger)

rf.close()          
wf.close()
print('Analyzing List Items is Finished ..... \n') 


print('Analyzing List Items is Started ..... \n')
wf = codecs.open(listTagging_path,encoding='utf-8',mode='w')
rf = codecs.open(list_path,encoding='utf-8',mode='r')

lineList = []
for line in rf.readlines() :
    lineItem = line.split('\t')
    title = lineItem[4]    
    desc = lineItem[5]    
    lineList.append(title + ' ' + desc)
    
## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
hangul_mining.start('pos', lineList, wf, logger)

rf.close()          
wf.close()
print('Analyzing List Items is Finished ..... \n') 
#
#
############################################################################
print('program is finished...Thanks...')    
#       
#
#
#   
#   
#   
#   
#   