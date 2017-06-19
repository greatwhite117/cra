# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import urllib
import requests

f=open('C:\\Users\\eunjin\\review_all.txt',mode='w')


url1 = 'http://movie.naver.com/movie/bi/mi/pointWriteFormList.nhn?code=121051'
url2 = '&type=after&isActuralPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page=' 

page = int(1)


while page < 4000 :

	url = url1+url2+str(page)

	open = urllib.urlopen(url)

	html=open.read().decode('utf-8')

	soup = BeautifulSoup(html, "lxml")

	score_result = soup.find('div',class_='score_result')

#link = soup.find_all("div", { "class" : "score_reple"})
#link = soup.find_all("div", { "class" : "score_reple"})


	lis = score_result.find_all('li')

	for li in lis :
		reple = li.find('div', class_='score_reple').find('p').get_text()
		score = li.find('div', class_='star_score').find('em').get_text()
		f.write('리뷰내용 : '+reple.encode('utf-8')+'\t')
		f.write('평점 : '+score.encode('utf-8')+'\n')

	f.write('\n')
	print("page "+str(page)+"complete")
	page += 1

f.close()

print("----the end-----")
#for m in link:
#
# print (m.string)
 