
from bs4 import BeautifulSoup

import urllib


f=open('C:\\Users\\eunjin\\dc_cos.txt',mode='w')

url = 'http://gall.dcinside.com/board/lists/?id=cosmetic&page='
page=int(1)

while page < 100:

	html = urllib.urlopen(url+str(page))

	soup = BeautifulSoup(html, "lxml")


	link = soup.find_all("a", { "class" : "icon_txt_n"})



	for m in link:

		print (m.string)

		f.write(m.string.encode('utf-8')+'\n')

	f.write('\n')

	print("page "+str(page)+"complete")
	page += 1

f.close()

print("----the end-----")