# -*- coding: utf-8 -*-

"""
Created on Tue Jul 05 09:44:42 2016

@author: sspark
"""

import sys
import logging
import codecs
from smba2_module import collect_naver, collect_news_body, collect_comments, hangul_mining
import datetime
import time

if len(sys.argv) > 1 : # 입력인자가 있을 경우
    crl_keyword = sys.argv[1]
    crl_cnt = int(sys.argv[2])
    crl_newsbody = sys.argv[3]   
    crl_comments = sys.argv[4] 
       
    crl_keyword = crl_keyword.decode('euc-kr')

   
else : #입력인자가 없을 경우 사용자 입력 받음
    print('\n////////////////////////////////////////////////////////////////////////////////')
    print('<키워드 기반 네이버 API (뉴스,블로그,카페) 수집 서비스>  Version 1.0, 2016.07.05\n')
    print('  - 네이버 뉴스의 제목과 원문 그리고 댓글, 조횟수, 좋아요 수를 수집합니다.' )
    print('  - 수집 종료 후 "명사", "의미단위", " 품사태깅"으로 각각 키워드 분석을 진행합니다.' )
    print('  - 수집 및 키워드 분석 결과는 "D:\\smba2_crawler\\result_api" 에서 확인 가능합니다.\n' )
    print('  - made by sspark')
    print('////////////////////////////////////////////////////////////////////////////////\n\n')
    
    crl_keyword  = raw_input("1. 수집할 단어 또는 문장을 입력하세요. ==> ")
    crl_cnt      =     input("2. 수집할 데이터 건수를 입력하세요. (1 ~ 1000)  ==> ")   
    crl_newsbody = raw_input("3. 네이버 뉴스 원문을 조회 하시겠습니까? (y/n) ==> ")
    crl_comments = raw_input("4. 관련 뉴스의 댓글도 조회 하시겠습니까? 작업이 오래 걸릴 수 있습니다. (y/n) ==> ")
    
    if len(crl_keyword) == 0 :
       crl_keyword = '브렉시트'
    if len(crl_newsbody) == 0:
       crl_newsbody = 'n'
    if len(crl_comments) == 0:
       crl_comments = 'y'  
       
    crl_keyword = crl_keyword.decode('utf-8')   
   


## step0. naver api key 설정 (각자의 키로 설정할 것)
api_id = 'qIDwAwAuX7L9EwgEEz2B'
api_secret = 'J1ydQKyp8V'

print('keyword ====> ' + crl_keyword + ' start....\n')

## step1. 저장할 파일 지정
base_path = 'C:\\smba2_crawler\\result_api\\'
list_path = base_path + crl_keyword + '_list.txt'  #뉴스, 블로그, 카페 통합 리스트
newsbody_path = base_path + crl_keyword + '_newsBody.txt' # 뉴스 원문
comments_path = base_path + crl_keyword + '_newsComments.txt' # 수집된 뉴스의 댓글

listNoun_path = base_path + crl_keyword + '_listNoun.txt' # 리스트 명사 분석
listPhrase_path = base_path + crl_keyword + '_listPhrase.txt' # 리스트 의미단위 분석
listTagging_path = base_path + crl_keyword + '_listTagging.txt' # 리스트 품사태깅 분석

comNoun_path = base_path + crl_keyword + '_comNoun.txt' # 댓글 명사 분석
comPhrase_path = base_path + crl_keyword + '_comPhrase.txt' # 댓글 의미단위 분석
comTagging_path = base_path + crl_keyword + '_comTagging.txt' # 댓글 품사태깅 분석

## step2. 로깅 파일 설정
fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
#log_path = base_path + crl_keyword + '_' + datetime.date.today().strftime('%Y-%m-%d') + '.log'
log_path = base_path + crl_keyword + '_' + '2015-03-16' + '.log'

logging.basicConfig(level='WARN', format=fmt, filename=log_path, filemode='w')
logging.basicConfig
logger = logging.getLogger('naver_api_crawler')


########################################################################### 
ing_cnt = 1
## step3. 뉴스, 블로그, 카페 통합 리스트 수집
wf = codecs.open(list_path,encoding='utf-8',mode='w')

print('Collecting Naver News is Started ..... \n')
#ing_cnt = collect_naver.start('news',api_id,api_secret,crl_keyword,crl_cnt,wf,list_path,logger,ing_cnt)

print('Collecting Naver News is finished .... \n\n')

print('Collecting Naver Blog is Started ..... \n')
#ing_cnt = collect_naver.start('blog',api_id,api_secret,crl_keyword,crl_cnt,wf,list_path,logger,ing_cnt)
print('Collecting Naver Blog is finished .... \n\n')

print('Collecting Naver cafe is Started ..... \n')
ing_cnt = collect_naver.start('cafearticle',api_id,api_secret,crl_keyword,crl_cnt,wf,list_path,logger,ing_cnt)
print('Collecting Naver cafe is finished .... \n\n')

wf.close()

########################################################################### 
## step4. 뉴스 원문 수집
if crl_newsbody == 'y' :    
    print('Collecting Naver News Body is Started ..... \n')
    wf = codecs.open(newsbody_path,encoding='utf-8',mode='w')
    rf = codecs.open(list_path,encoding='utf-8',mode='r')
       
    for line in rf.readlines() :
        lineItem = line.split('\t')
        api_type = lineItem[2]     
        if api_type == 'news' :
            collect_news_body.start(line, wf, logger)
     
    rf.close()          
    wf.close()
    print('Collecting Naver News Body is Finischemad ..... \n')
   
ing_cnt = 1   
## step5. 관련 뉴스 댓글 수집
if crl_comments == 'y' :    
    print('Collecting Naver News comments is Started ..... \n')
    
    wf = codecs.open(comments_path,encoding='utf-8',mode='w')
    rf = codecs.open(list_path,encoding='utf-8',mode='r')
    
    for line in rf.readlines() :
        lineItem = line.split('\t')
        api_type = lineItem[2]    
        comments_cnt = lineItem[7]
        if api_type == 'news' and comments_cnt <> '0' :
            time.sleep(1)
            ing_cnt = collect_comments.start('api',line, wf, logger, ing_cnt)
     
    rf.close()          
    wf.close()
    
    print('Collecting Naver News comments is Finished ..... \n')
    

############################################################################   
## step6. 리스트 키워드 분석   
print('Analyzing List Items is Started ..... \n')
wf = codecs.open(listNoun_path,encoding='utf-8',mode='w')
rf = codecs.open(list_path,encoding='utf-8',mode='r')

lineList = []
for line in rf.readlines() :
    lineItem = line.split('\t')
    title = lineItem[10]    
    desc = lineItem[11]    
    lineList.append(title + ' ' + desc)
    
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
    title = lineItem[10]    
    desc = lineItem[11]    
    lineList.append(title + ' ' + desc)
    
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
    title = lineItem[10]    
    desc = lineItem[11]    
    lineList.append(title + ' ' + desc)
    
## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
hangul_mining.start('pos', lineList, wf, logger)

rf.close()          
wf.close()
print('Analyzing List Items is Finished ..... \n') 


###########################################################################
## step7. 댓글 키워드 분석   
if crl_comments == 'y' :
    print('Analyzing comments is Started ..... \n')
    wf = codecs.open(comNoun_path,encoding='utf-8',mode='w')
    rf = codecs.open(comments_path,encoding='utf-8',mode='r')
    
    lineList = []
    for line in rf.readlines() :
        lineItem = line.split('\t')
        text = lineItem[1]        
        lineList.append(text)
        
    ## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
    hangul_mining.start('noun', lineList, wf, logger)
    
    rf.close()          
    wf.close()
    print('Analyzing comments is Finished ..... \n')   
    
    print('Analyzing comments is Started ..... \n')
    wf = codecs.open(comPhrase_path,encoding='utf-8',mode='w')
    rf = codecs.open(comments_path,encoding='utf-8',mode='r')
    
    lineList = []
    for line in rf.readlines() :
        lineItem = line.split('\t')
        text = lineItem[1]        
        lineList.append(text)
        
    ## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
    hangul_mining.start('phrase', lineList, wf, logger)
    
    rf.close()          
    wf.close()
    print('Analyzing comments is Finished ..... \n') 
    
    
    print('Analyzing comments is Started ..... \n')
    wf = codecs.open(comTagging_path,encoding='utf-8',mode='w')
    rf = codecs.open(comments_path,encoding='utf-8',mode='r')
    
    lineList = []
    for line in rf.readlines() :
        lineItem = line.split('\t')
        text = lineItem[1]        
        lineList.append(text)
        
    ## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
    hangul_mining.start('pos', lineList, wf, logger)
    
    rf.close()          
    wf.close()
    print('Analyzing comments is Finished ..... \n') 
    
print('\n\n############################\n')
print('program is finished...Thanks...')    
       


   
   
   
   
   