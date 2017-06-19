def get web('url'):
	URL을 넣으면 페이지 내용을 올려주는 함구***
	import urllib.request 
	response = urllib.request.urlopen(url)
	data = response.read()
	decoded = data.decode('utf-8') 
	return decided 
	
url = input('웹페이지 주소?)
content = get web(url)
