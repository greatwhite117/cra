< 빅데이터2기(smba2) 인터넷 정보 수집 프로그램 >
- version : 1.0
- update  : 2016.07.06
- made by : sspark
- scope   : naver api, news, blog, cafe, twitter, knlp

1. 개발 및 실행 환경
 - windows 10 64 비트
 - anaconda2(64bit) with python2.7

2. 크롬 드라이버 설치
 - pip install selenium
 - D:\smba2_crawler\tools\chromedriver.exe
   -> C:\Windows\System32\chrom webdrive 복사
 => https://sites.google.com/a/chromium.org/chromedriver/downloads 참조

3. 한글 형태소 분석기 설치
 - java 1.7+ 설치
 - java_home 설정
 - pip install --upgrade pip
 - pip install D:\smba2_crawler\tools\JPype1-0.6.1-cp27-none-win_amd64.whl
 - pip install konlpy
 => http://konlpy.org/ko/v0.4.3/install/#id2 windows 부문 참고

4. 트위터 API 설치
  - pip install tweepy

5. 실행방법
  5.1 네이버 API 수집
     - 실행전 본인의 네이버 api 계정과 패스워드로 수정할 것
        * D:\smba2_crawler>python naver_api_crawler.py
         # api_id = 'qIDwAwAuX7L9EwgEEz2B' <- 변경
         # api_secret = 'J1ydQKyp8V' <- 변경
     - 첫번째> windows 명령어 프롬프트 에 작업 걸어놓기
        * D:\smba2_crawler>python naver_api_crawler.py 브렉시트 100 y y
          # 파라미터1 : 검색할 키워드
          # 파라미터2 : 수집할 건수 (1 ~ 1000, naver api 최대 1000개 까지만 가능)  
          # 파라미터3 : 뉴스 본문 수집 여부 (y/n)
          # 파라미터4 : 뉴스 댓글 수집 여부 (y/n)
     - 두번째> 아나콘다 iPython 에서 naver_api_crawler.py 실행 
        * 지시에 따라 수행

  5.2 네이버 WEB 수집
     - 첫번째> windows 명령어 프롬프트 에 작업 걸어놓기
        * D:\smba2_crawler>python naver_web_crawler.py 브렉시트 2016-07-05 2016-07-06 100 y y
          # 파라미터1 : 검색할 키워드
	  # 파라미터2 : 검색 시작일
	  # 파라미터3 : 검색 종료일
          # 파라미터4 : 수집할 건수 (0일 경우 지정기간 전체 수집) 
          # 파라미터5 : 뉴스 본문 수집 여부 (y/n)
          # 파라미터6 : 뉴스 댓글 수집 여부 (y/n)
     - 두번째> 아나콘다 iPython 에서 naver_web_crawler.py 실행 
        * 지시에 따라 수행

  5.3 트위터 스트리밍 수집
     - 실행전 본인의 트위터 api 계정과 패스워드로 수정할 것
        * D:\smba2_crawler>python tweeter_streaming.py
	  # consumer_key='cciVC37i1f7zQ3ucGqIuDv2xh'
	  # consumer_secret='dDzYkf95wu741aAC8Cwl3fKj7DLHfL5a9oAeWOBKGaGgag4nQg'
	  # access_token="164612747-93EjyQQ7pCyEiU0Tl7rLKhCnIW0kSCEJjoDKFbLG"
	  # access_token_secret='qajekc1r6ThOBgYRsZ1Ivz31cFxEsKriZxLolrurPsmnT'
     - windows 명령어 프롬프트 에 작업 걸어놓기
       * D:\smba2_crawler>python tweeter_streaming.py mudo_tweeter.txt 무한도전 무도 무랭이
          # 파라미터1 : 저장할 파일명
          # 파라미터2 ~ N : 수집할 키워드

6. 결과확인
 - D:\smba2_crawler\result_XXX 디렉토리에 키워드별로 저장된 결과 파일 확인
 - 엑셀로 열어서 확인

