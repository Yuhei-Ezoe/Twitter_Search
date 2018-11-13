#!/usr/bin/env python
# coding: utf-8

# In[2]:


import tweepy

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
count = 100


#メイン処理
tweet = []
search_results = api.search(q=search_word, count=count)

for search_result in search_results:
    tweet.append ("・" + search_result.text)

print(tweet[:5])


# In[ ]:




