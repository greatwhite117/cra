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


if len(sys.argv) > 1 : # 입력인자가 있을 경우
    crl_keyword = sys.argv[1]
    crl_keyword = crl_keyword.decode('euc-kr')

   
else : #입력인자가 없을 경우 사용자 입력 받음
    print('\n////////////////////////////////////////////////////////////////////////////////')
    print('<키워드 기반 네이버 WEB 뉴스 수집 서비스>  Version 1.0, 2016.07.05\n')
    print('  - 네이버 뉴스의 제목과 원문 그리고 댓글, 조횟수, 좋아요 수를 수집합니다.' )
    print('  - 수집 종료 후 "명사", "의미단위", " 품사태깅"으로 각각 키워드 분석을 진행합니다.' )
    print('  - 수집 및 키워드 분석 결과는 "D:\\smba2_crawler\\result" 에서 확인 가능합니다.\n' )
    print('  - made by sspark')
    print('////////////////////////////////////////////////////////////////////////////////\n\n')
    
    crl_keyword  = raw_input("1. 수집할 단어 또는 문장을 입력하세요. ==> ")
    
    if len(crl_keyword) == 0 :
       crl_keyword = '가짜뉴스'
       
    crl_keyword = crl_keyword.decode('ISO-8859-1')   
   


print('keyword ====> ' + crl_keyword + ' start....\n')


## step1. 저장할 파일 지정
base_path = 'C:\\smba2_crawler\\result_web\\'
list_path = base_path + crl_keyword + '_list.txt'  #뉴스, 블로그, 카페 통합 리스트
newsbody_path = base_path + crl_keyword + '_newsBody.txt' # 뉴스 원문

## step2. 로깅 파일 설정
fmt = '%(asctime)s %(levelname)s %(lineno)s %(message)s'
log_path = base_path + crl_keyword + '_' + datetime.date.today().strftime('%Y-%m-%d') + '.log'
logging.basicConfig(level='WARN', format='fmt', filename='log_path', filemode='w')
logging.basicConfig
logger = logging.getLogger('naver_web_crawler')


########################################################################### 
## step4. 뉴스 원문 수집
print('Collecting Naver News Body is Started ..... \n')
wf = codecs.open(newsbody_path,encoding='utf-8',mode='w')
rf = codecs.open(list_path,encoding='utf-8',mode='r')
       
for line in rf.readlines() :
    lineItem = line.split('\t')
    time.sleep(1)
    if not lineItem[6] is None and len(lineItem[6]) > 10 :
        collect_news_body.start_web(line, wf, logger)
     
rf.close()          
wf.close()
print('Collecting Naver News Body is Finished ..... \n')
#   
