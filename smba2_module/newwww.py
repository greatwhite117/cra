
from bs4 import BeautifulSoup

import urllib


html = urllib.urlopen('http://gall.dcinside.com/board/lists/?id=chinese')

soup = BeautifulSoup(html, "lxml")


link = soup.find_all("a", { "class" : "icon_txt_n"})




for m in link:

 print (m.string)
 