# -*- coding: utf-8 -*-
"""
Created on Sun Jul 03 16:27:40 2016

@author: sspark
"""
from __future__ import print_function
from konlpy.tag import Twitter
#from konlpy.utils import pprint
from collections import Counter

def start(ays_type, sentences, wf, logger) :
    analysis_type = ays_type ## noun:명사분석, phrase:의미단위분석, pos:품사태깅    
  
    twitter = Twitter() ## 트위터에서 만든 한국어 형태소 분석기    
    
    ## analysis 1 : 명사 분석
    if analysis_type == 'noun' :
        cnt = 1
        nounsDic={}
        
        for sentence in sentences :
            nouns = twitter.nouns(sentence) ## 명사만 추출
            for noun in nouns:
                if noun in nounsDic: ## 있다면 +1
                   now_cnt = nounsDic[noun]
                   nounsDic[noun] = now_cnt + 1
                else: ## 없다면 추가
                    nounsDic[noun] = 1
            print('sentence(' + str(cnt) + ') analyzing......')   
            cnt = cnt + 1           
        
        nounsCounter = Counter(nounsDic).most_common() # 내림차순 정렬 반환값 [(key,value), (key,value)]
        #print(nounsCounter)    
        
        for key, value in nounsCounter :
            #print(key + ' // ' + str(value))
            if value >= 10 :
                wf.write(key + '\t' + str(value) + '\n')        
               
    #    for key in nounsDic.keys():
    #        #print(key + ' // ' + str(nounsDic[key]))
    #        wf.write(key + '\t' + str(nounsDic[key]) + '\n')
        
        print('sentences analysis is finished....')
    
    ## analysis 2 : 의미단위 분석
    if analysis_type == 'phrase' :
        phrasesDic={}
        cnt = 1
        
        for sentence in sentences :
            phrases = twitter.phrases(sentence) ## 의미단위 추출
            for phrase in phrases:
                if phrase in phrasesDic: ## 있다면 +1
                   now_cnt = phrasesDic[phrase]
                   phrasesDic[phrase] = now_cnt + 1
                else: ## 없다면 추가
                    phrasesDic[phrase] = 1
            print('sentence(' + str(cnt) + ') analyzing......')   
            cnt = cnt + 1
        
        phrasesCounter = Counter(phrasesDic).most_common() # 내림차순 정렬 반환값 [(key,value), (key,value)]
        #print(nounsCounter)    
        
        for key, value in phrasesCounter :
            #print(key + ' // ' + str(value))
            if value >= 10 :
                wf.write(key + '\t' + str(value) + '\n')      
                
    #    for key in phrasesDic.keys():
    #        #print(key + ' // ' + str(phrasesDic[key]))
    #        wf.write(key + '\t' + str(phrasesDic[key]) + '\n')
            
        print('sentences analysis is finished....')
  
    
    ## analysis 3 : 품사 태깅 분석
    if analysis_type == 'pos' :
        posesDic={}
        cnt = 1
        
        for sentence in sentences :
            poses = twitter.pos(sentence,norm=True,stem=True) ## 품사태깅
            for pos in poses:
                if pos in posesDic: ## 있다면 +1
                   now_cnt = posesDic[pos]
                   posesDic[pos] = now_cnt + 1
                else: ## 없다면 추가
                    posesDic[pos] = 1
            print('sentence(' + str(cnt) + ') analyzing......')   
            cnt = cnt + 1
        
        posesCounter = Counter(posesDic).most_common() # 내림차순 정렬 반환값 [(key,value), (key,value)]
        #print(nounsCounter)    
        
        for key, value in posesCounter :
            noun, tagging = key
            #print(noun + ' // ' + tagging + '//' + str(posesDic[key]))
            if value >= 10 :
                wf.write(noun + '\t' + tagging + '\t' + str(value) + '\n')     
         
    #    for key in posesDic.keys():
    #        noun, tagging = key
    #        #print(noun + ' // ' + tagging + '//' + str(posesDic[key]))
    #        wf.write(noun + '\t' + tagging + '\t' + str(posesDic[key]) + '\n')
            
        print('sentences analysis is finished....')





