#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
search_word = ["***", "***", "***", "***", "***"]
#何件検索表示するか
count = 100


#メイン処理

i = 0
while i < len(search_word):
    search_results = api.search(q=search_word[i], count=count)
    
    #各々のデータを保存するリストを設定
    result_tweet_time = []
    result_name = []
    result_user_name = []
    result_tweet = []
    result_follow_count = []
    result_follower_count = []
    result_ff_ratio = []
        
        
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
    
    
    
        #フォロー数を取得
        follow_count = search_result.user.friends_count
    
        #リストに保存
        result_follow_count.append(follow_count)
    
    
    
        #フォロワー数を取得
        follower_count = search_result.user.followers_count
    
        #リストに保存
        result_follower_count.append(follower_count)
    
    
    
        #フォロー・フォロワー比を計算
        #フォロワー数が0の時を考慮
        if follow_count != 0:
            
            ff_ratio = follower_count / follow_count
    
            #リストに保存
            result_ff_ratio.append(ff_ratio)
    
        else:
            ff_ratio = 0
            
            #リストに保存
            result_ff_ratio.append(ff_ratio)
           
            

    #それぞれのデータを1つの表にまとめる
    df = pd.DataFrame({
        "ツイート日時" : result_tweet_time,
        "名前" : result_name,
        "ユーザー名" : result_user_name,
        "ツイート" : result_tweet,
        "フォロー数" : result_follow_count,
        "フォロワー数" : result_follower_count,
        "フォロー・フォロワー比" : result_ff_ratio
    })

    #表の列の順番を指定(行は指定しないので番号が割り振られる)
    df.columns = [
        "ツイート日時",
        "名前",
        "ユーザー名",
        "ツイート",
        "フォロー数",
        "フォロワー数",
        "フォロー・フォロワー比"
    ]

    #フォロワー数が100以上 (filter1) のユーザーを抜き出す
    df_filter1 = df[df["フォロワー数"] >= 100]
    
    #さらにフォロー・フォロワー比が1以上 (filter2) のユーザーを表から抜き出す
    df_filter2 = df_filter1[df_filter1["フォロー・フォロワー比"] >= 1]

    
    #df_filter2の表からユーザー名を抜き出し、ツイッタープロフィールのURLを作成する
    #まず、上記条件を満たしたユーザー名を表から抜き出しリスト化
    user_list = df_filter2["ユーザー名"].tolist()
    
    #各ツイッタープロフィールページのURLをリスト化
    user_url = []
    n = 0
    while n < len(user_list):
        user_url.append("https://twitter.com/" + user_list[n]+ "?lang=ja")
        
        n += 1
    
    #df_filter2にプロフィールURLの列を追加し、csvファイルで出力
    df_filter2["プロフィールURL"] = user_url
    df_filter2.to_csv("result_twitter-{}.csv".format("[" + str(i) + "] " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M")))
    
    
    i += 1

