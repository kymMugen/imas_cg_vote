# coding: utf-8

from datetime import datetime
import pytz
from peewee import fn
from twitter_auth import api
from model import db, Idol, Tweet, Count


def count(timestamp):
    count_data = []

    for idol in Idol.select(Idol.name):
        tweet_count = Tweet.select().where(
            Tweet.tweet_text % ('%' + idol.name + '%')).count()

        user_count = Tweet.select(fn.Distinct(Tweet.user_id)).where(
            Tweet.tweet_text % ('%' + idol.name + '%')).wrapped_count()

        count_data.append({
            'name': idol.name,
            'timestamp': timestamp,
            'tweet_count': tweet_count,
            'user_count': user_count
        })

    try:
        with db.transaction():
            Count.insert_many(count_data).execute()

    except:
        db.rollback()


def tweet_count_tweet(attr, timestamp):
    if attr == '全属性':
        idols = Count.select().where(
            Count.timestamp == timestamp).order_by(
            Count.tweet_count.desc()).limit(10)
    else:
        idols = Count.select(Count, Idol).join(Idol).where(
            Count.timestamp == timestamp, Idol.attribute == attr).order_by(
            Count.tweet_count.desc()).limit(10)

    tweet = '【' + timestamp + '】総投票ツイート数：' + attr + '\n'

    counter = 1

    for idol in idols:
        tweet += str(counter) + '. ' + idol.name_id + \
            '（' + str(idol.tweet_count) + '）\n'

        if counter == 5 or counter == 10:
            tweet += '#シンデレラガール総選挙'
            api.update_status(status=tweet)
            tweet = '【' + timestamp + '】総投票ツイート数：' + attr + '\n'

        counter += 1


def user_count_tweet(attr, timestamp):
    if attr == '全属性':
        idols = Count.select().where(
            Count.timestamp == timestamp).order_by(
            Count.user_count.desc()).limit(10)
    else:
        idols = Count.select(Count, Idol).join(Idol).where(
            Count.timestamp == timestamp, Idol.attribute == attr).order_by(
            Count.user_count.desc()).limit(10)

    tweet = '【' + timestamp + '】総投票ツイート数（ユーザ重複を除く）：' + attr + '\n'

    counter = 1

    for idol in idols:
        tweet += str(counter) + '. ' + idol.name_id + \
            '（' + str(idol.user_count) + '）\n'

        if counter == 5 or counter == 10:
            tweet += '#シンデレラガール総選挙'
            api.update_status(status=tweet)
            tweet = '【' + timestamp + '】総投票ツイート数（ユーザ重複を除く）：' + attr + '\n'

        counter += 1


def main():
    utc_now = datetime.now(pytz.timezone('UTC'))
    jst_now = utc_now.astimezone(pytz.timezone('Asia/Tokyo'))
    timestamp = jst_now.strftime('%Y-%m-%d %H:%M:%S')

    count(timestamp)
    for attr in ['全属性', 'Cu', 'Co', 'Pa']:
        tweet_count_tweet(attr, timestamp)
        user_count_tweet(attr, timestamp)


if __name__ == '__main__':
    main()
