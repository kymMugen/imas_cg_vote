# coding: utf-8

from time import sleep
from datetime import datetime
import pytz
from peewee import fn
from twitter_auth import api
from model import db, Tweet, Update


def extract_tweet(tweet):
    timestamp_utc = pytz.utc.localize(tweet.created_at)
    timestamp_jst = timestamp_utc.astimezone(pytz.timezone('Asia/Tokyo'))
    tweet_data = {'tweet_id': tweet.id,
                  'tweet_text': tweet.text,
                  'user_id': tweet.author.id,
                  'timestamp': timestamp_jst.strftime('%Y-%m-%d %H:%M:%S')
                  }
    return tweet_data


def main():
    query = '投票したよ!! http://sp.pf.mbga.jp/12008305/ ' \
            '#シンデレラガール総選挙 exclude:retweets'
    count = 100
    since_id = 0
    max_id = None

    if Tweet.select().count() > 0:
        since_id = int(Update.select().order_by(
                Update.last_update.desc()).limit(1)[0].tweet_id_id) + 1

    tweet_data_list = []

    counter = 0
    while True:
        search_result = api.search(
            q=query,
            count=count,
            since_id=since_id,
            max_id=max_id
        )

        if len(search_result) == 0:
            print('end')
            break

        for tweet in search_result:
            if tweet.source == 'アイドルマスター シンデレラガールズ公式':
                tweet_data_list.append(extract_tweet(tweet))

        max_id = search_result[-1].id - 1
        counter += 1
        print(counter)
        if counter == 150:
            counter = 0
            sleep(900)

    try:
        with db.transaction():
            Tweet.insert_many(tweet_data_list).execute()

    except:
        db.rollback()

    last_id = Tweet.select(Tweet.tweet_id).order_by(
        Tweet.timestamp.desc()).limit(1)[0].tweet_id

    utc_now = datetime.now(pytz.timezone('UTC'))
    jst_now = utc_now.astimezone(pytz.timezone('Asia/Tokyo'))

    try:
        with db.transaction():
            Update.insert(
                tweet_id=last_id,
                last_update=jst_now.strftime('%Y-%m-%d %H:%M:%S')
            ).execute()

    except:
        db.rollback()

if __name__ == '__main__':
    main()
