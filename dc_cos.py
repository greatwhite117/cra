# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup

import urllib
import requests

f=open('C:\\Users\\eunjin\\dc_cos.txt',mode='w')

url1 = 'http://gall.dcinside.com/board/lists/?id=cosmetic&page='
page=int(1)

f.write('date'+'\t')
f.write('title'+'\n')

while page < 500 :

	url = url1+str(page)
	print url

	open = urllib.urlopen(url)

	html=open.read().decode('utf-8')

	soup = BeautifulSoup(html, "lxml")


	dc_result = soup.find('tbody',class_='list_tbody')



	lis = dc_result.find_all('tr')

	print lis


	for li in lis :
		date = li.find('td', class_='t_date').get_text()
		title = li.find('td', class_= 't_subject').get_text()

		f.write(date.encode('utf-8')+'\t')
		f.write(title.encode('utf-8')+'\n')

	f.write('\n')
	print("page "+str(page)+"complete")
	page += 1

f.close()

print("----the end-----")