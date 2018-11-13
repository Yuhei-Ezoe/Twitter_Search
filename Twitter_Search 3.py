#!/usr/bin/env python
# coding: utf-8

# In[23]:


import tweepy
import time
import calendar
import pandas as pd
import datetime

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
#各々のデータを保存するリストを設定
result_tweet_time = []
result_name = []
result_user_name = []
result_tweet = []

search_results = api.search(q=search_word, count=count)

for search_result in search_results:
    
    
    #ツイート日時取得(※世界標準時)
    tweet_time = search_result.created_at
    
    #日本時間に変更
    #取得できる日付(世界標準時)をそれぞれの要素に分解(struct_timeという)
    divided_time = time.strptime(str(tweet_time), "%Y-%m-%d %H:%M:%S")
    
    #struct_timeからunix_timeに変換
    unix_time = calendar.timegm(divided_time)
    
    #unix_timeから日本時間(struct_time)に変換
    jp_divided_time = time.localtime(unix_time)
    
    #好きな表示形式に変換
    jp_time = time.strftime("%Y-%m-%d %H:%M:%S", jp_divided_time)
    
    #リストに保存
    result_tweet_time.append(jp_time)
    
    
    
    
    #名前を取得
    name = search_result.user.name
    
    #リストに保存
    result_name.append(name)
    
    
    
    
    #ユーザー名を取得
    user_name = search_result.user.screen_name
    
    #リストに保存
    result_user_name.append(user_name)
    
    
    
    #ツイート本文を取得
    tweet = search_result.text
    
    #リストに保存
    result_tweet.append(tweet)
    

#それぞれのデータを1つの表にまとめる
df = pd.DataFrame({
    "ツイート日時" : result_tweet_time,
    "名前" : result_name,
    "ユーザー名" : result_user_name,
    "ツイート" : result_tweet
})

#表の列の順番を指定(行は指定しないので番号が割り振られる)
df.columns = [
    "ツイート日時",
    "名前",
    "ユーザー名",
    "ツイート"
]

#結果をcsvファイルで出力
df.to_csv("result_twitter-{}.csv".format(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))

print(df["ツイート"])

