# -*- coding: utf-8 -*-


import sys
import logging
import codecs
from cra_module import collect_naver, collect_news_body, hangul_mining
import datetime
import time

if len(sys.argv) > 1 : # 입력인자가 있을 경우
    crl_keyword = sys.argv[1]
    crl_cnt = int(sys.argv[2])
    crl_newsbody = sys.argv[3]   
       
    crl_keyword = crl_keyword.decode('euc-kr')

   
else : #입력인자가 없을 경우 사용자 입력 받음
    print("입력인자를 넣지 않으셨습니다.")
    return 0;  
          


## step0. naver api key 설정 (각자의 키로 설정할 것)
api_id = 'qIDwAwAuX7L9EwgEEz2B'
api_secret = 'J1ydQKyp8V'

print('keyword ====> ' + crl_keyword + ' start....\n')



## step1. 저장할 파일 지정
base_path = 'C:\\smba2_crawler\\result_api\\'
list_path = base_path + crl_keyword + '_list.txt'  #뉴스, 블로그, 카페 통합 리스트
newsbody_path = base_path + crl_keyword + '_newsBody.txt' # 뉴스 원문

listNoun_path = base_path + crl_keyword + '_listNoun.txt' # 리스트 명사 분석
listPhrase_path = base_path + crl_keyword + '_listPhrase.txt' # 리스트 의미단위 분석
listTagging_path = base_path + crl_keyword + '_listTagging.txt' # 리스트 품사태깅 분석



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
ing_cnt = collect_naver.start('news',api_id,api_secret,crl_keyword,crl_cnt,wf,list_path,logger,ing_cnt)

print('Collecting Naver News is finished .... \n\n')

print('Collecting Naver Blog is Started ..... \n')
ing_cnt = collect_naver.start('blog',api_id,api_secret,crl_keyword,crl_cnt,wf,list_path,logger,ing_cnt)
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
    print('Collecting Naver News Body is Finished ..... \n')
   
ing_cnt = 1   



############################################################################   
## step5. 리스트 키워드 분석   
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


    
print('\n\n############################\n')
print('program is finished...Thanks...')    
       


   
   
   
   
   