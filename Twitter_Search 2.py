#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tweepy
import time
import calendar

CONSUMER_KEY = "***"
CONSUMER_SECRET = "***"
ACCESS_TOKEN = "***"
ACCESS_SECRET = "***"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)

#検索ワード設定
search_word = "***"
#何件検索表示するか
count = 5

#メイン処理
search_results = api.search(q=search_word, count=count)

for search_result in search_results:
    #ツイート日時取得(※世界標準時)
    tweet_time = search_result.created_at
    print("世界標準時 : " + str(tweet_time))
    
    #日本時間に変更
    #取得できる日付(世界標準時)をそれぞれの要素に分解(struct_timeという)
    divided_time = time.strptime(str(tweet_time), "%Y-%m-%d %H:%M:%S")
    
    #struct_timeからunix_timeに変換
    unix_time = calendar.timegm(divided_time)
    
    #unix_timeから日本時間(struct_time)に変換
    jp_divided_time = time.localtime(unix_time)
    
    #好きな表示形式に変換
    jp_time = time.strftime("%Y-%m-%d %H:%M:%S", jp_divided_time)
    
    print("日本時間 : " + jp_time)
    
    
    #名前を取得
    name = search_result.user.name
    print("名前 : " +name)
    
    #ユーザー名を取得
    user_name = search_result.user.screen_name
    print("ユーザー名 : @" + user_name)
    
    #ツイート本文を取得
    tweet = search_result.text
    print("ツイート : " + tweet)
    
    print("----------------------------------------------")

