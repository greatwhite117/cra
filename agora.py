# -*- coding: cp949 -*-

import urllib2
from bs4 import BeautifulSoup
import codecs
from lxml import etree

# agora.txt 파일에다가 내용 다 넣을 것입니다.
f=open("agora.txt", 'w')

for num in range(4836698, 4838698): # 특정 게시글 번호만을 추출, 이 번호에 따라서 퍼올 게시글 번호가 바뀌어진다.
    url = "http://bbs1.agora.media.daum.net/gaia/do/debate/read?articleId=" + str(num) + "&bbsId=D101&pageIndex=1"

    page = urllib2.urlopen(url)

    soup = BeautifulSoup(page, "lxml")
    #soup = BeautifulSoup(page)

    data = soup.select("[class~=tx-content-container]") # class~=tx-content-container 부분만 추출 (필요없는 다른 태그들 버림)
    data = str(data)

    print data

    f.write(data + "\n\n\n\n\n") # 각 게시글 구분

f.close()

# 문자열 인코딩, 디코딩 관련 작업
f1=codecs.open("temp.txt", 'r', encoding='utf-8')
f2=codecs.open("agora.txt", 'w')

data = f1.read()
data = data.encode('cp949', 'ignore')

f2.write(data)

f1.close()
f2.close()