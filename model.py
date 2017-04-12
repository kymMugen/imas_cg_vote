# coding: utf-8

import peewee
from db_settings import db


class Base(peewee.Model):
    class Meta:
        database = db


class Tweet(Base):
    tweet_id = peewee.TextField(primary_key=True)
    tweet_text = peewee.TextField()
    user_id = peewee.TextField()
    timestamp = peewee.DateTimeField()


class Idol(Base):
    name = peewee.TextField(primary_key=True)
    attribute = peewee.TextField()


class Count(Base):
    name = peewee.ForeignKeyField(rel_model=Idol, related_name='names')
    timestamp = peewee.DateTimeField()
    tweet_count = peewee.IntegerField()
    user_count = peewee.IntegerField()

    class Meta:
        primary_key = peewee.CompositeKey('name', 'timestamp')


class Update(Base):
    tweet_id = peewee.ForeignKeyField(rel_model=Tweet)
    last_update = peewee.DateTimeField()

    class Meta:
        primary_key = peewee.CompositeKey('tweet_id')
