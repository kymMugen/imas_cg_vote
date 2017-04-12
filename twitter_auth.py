# coding: utf-8

import os
import tweepy

try:
    import settings_local
    consumer_key = settings_local.CONSUMER_KEY
    consumer_secret = settings_local.CONSUMER_SECRET
    access_token = settings_local.ACCESS_TOKEN
    access_secret = settings_local.ACCESS_SECRET

except:
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_secret = os.environ['ACCESS_SECRET']


twitter_auth = tweepy.OAuthHandler(
    consumer_key,
    consumer_secret
)

twitter_auth.set_access_token(
    access_token,
    access_secret
)

api = tweepy.API(twitter_auth)
