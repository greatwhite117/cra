# -*- coding: utf-8 -*-
"""
cp949
Created on Sun Jul 03 16:27:40 2016

@author: sspark
"""

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import codecs  
import sys

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key='cciVC37i1f7zQ3ucGqIuDv2xh'
consumer_secret='dDzYkf95wu741aAC8Cwl3fKj7DLHfL5a9oAeWOBKGaGgag4nQg'

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token="164612747-93EjyQQ7pCyEiU0Tl7rLKhCnIW0kSCEJjoDKFbLG"
access_token_secret='qajekc1r6ThOBgYRsZ1Ivz31cFxEsKriZxLolrurPsmnT'

exclusive_text=['포르노','야동','광고','안마', '도신','채팅','변녀'] # 불용어 목록

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        print('It is tweet...')
        try :
            data = json.loads(data) 
           
            msg = data['text'].replace('\n',' ')
            for text in exclusive_text :
                text = text.decode('utf-8')
                if msg.find(text) >= 0 : #불용어 제외
                   print('Tweet...is excluded')
                   #counter = counter + 1
                   return True
   
            date = data['created_at']
            cdate = date[-4:] + '-' + set_month(date[4:7]) + '-' + date[8:10] + ' ' + date[11:19]            
            text = msg + '\t' + data['id_str'] + '\t' + data['lang'] + '\t' + cdate + '\n'
            print(data['id_str'] , 'Tweet..is writing...')
            wf.write(text)
            
        except Exception as ex :
            print('Tweet exception', ex)  
            return True       
  
        return True

    def on_error(self, status):    
        print( status, 'Error')
        wf.close() 
        return False

        
   
def set_month(mm) :
    if mm == 'Jan' :
        return '01'
    elif mm == 'Feb' :
        return '02'
    elif mm == 'Mar' :
        return '03'
    elif mm == 'Apr' :
        return '04'        
    elif mm == 'May' :
        return '05'        
    elif mm == 'Jun' :
        return '06'
    elif mm == 'Jul' :
        return '07'
    elif mm == 'Aug' :
        return '08'
    elif mm == 'Sep' :
        return '09'
    elif mm == 'Oct' :
        return '10'        
    elif mm == 'Nov' :
        return '11'        
    elif mm == 'Dec' :
        return '12'    
        
if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
   
    
    stream = Stream(auth, l)
    
    wordList = []    
    arvs = sys.argv
    if len(arvs) > 1 :
        
        for arv in arvs[2:] :
            print('keyword ==> ' + arv + '\n')
            word1 = arv.decode('euc-kr')
            word1 = word1.encode('utf-8')
            wordList.append(word1.decode('utf-8'))
        
        base_path = 'D:\\smba2_crawler\\result_tweeter\\'
        filename = base_path + arvs[1]
        wf=codecs.open(filename, encoding='utf-8', mode='w') 
        print(filename)
        
        stream.filter(track=wordList)     

    else :
        wf=codecs.open('D:\\smba2_crawler\\result\\tweeter_list.txt', encoding='utf-8', mode='w')         
        stream.filter(track=['밤샘대기'.decode('utf-8'), '무도'.decode('utf-8')])
        

    
    
    
