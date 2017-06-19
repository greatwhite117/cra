# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import urllib
import requests

f=open('C:\\Users\\eunjin\\review_samp1.txt',mode='w')


url1 = 'https://search.naver.com/search.naver?where=article&query=%EC%97%90%EB%9B%B0%EB%93%9C&ie=utf8&st=rel'
url2 = '&date_option=0&date_from=&date_to=&board=&srchby=text&dup_remove=1&cafe_url=cafe.naver.com%2Fcosmania&without_cafe_url=&sm=tab_opt&nso=&t=0&mson=0&prdtype=0&start=' 



page = int(1)


while page < 5 :

	url = url1+url2+str(1)
	print url
	open = urllib.urlopen(url)

	html=open.read().decode('utf-8')
	print html
	soup = BeautifulSoup(html, "lxml")
	print soup
	cafe_result = soup.find('ul',class_='type01')
	#soup.find('ul',class_='type01')

#link = soup.find_all("div", { "class" : "score_reple"})
#link = soup.find_all("div", { "class" : "score_reple"})
	print cafe_result

	lis = cafe_result.find_all('dl')
	print lis

	for li in lis :
		title = li.find('a', class_='sh_cafe_title').get_text()
		passage = li.find('dd', class_='sh_cafe_passage').find('dt').get_text()
		f.write('제목 : '+reple.encode('utf-8')+'\t')
		f.write('내용 : '+score.encode('utf-8')+'\n')

	f.write('\n')
	print("page "+str(page)+"complete")
	page += 1

f.close()

print("----the end-----")
#for m in link:
#
# print (m.string)
 