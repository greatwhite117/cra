# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import urllib
import requests

html = urllib.urlopen('http://movie.naver.com/movie/bi/mi/point.nhn?code=121051')

soup = BeautifulSoup(html, "lxml")

f=open('C:\\Users\\eunjin\\review.txt',mode='w')
score_result = soup.find('div',class_='score_result')

#link = soup.find_all("div", { "class" : "score_reple"})


#link = soup.find_all("div", { "class" : "score_reple"})


lis = score_result.find_all('li')

for li in lis :
	reple = li.find('div', class_='score_reple').find('p').get.text()
	f.write('리뷰내용 : '+reple.encode('utf-8')+'\t')

f.close()

print("----the end-----")
#for m in link:
#
# print (m.string)
 