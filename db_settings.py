# coding: utf-8


import os
from peewee import PostgresqlDatabase

try:
    import settings_local
    database = settings_local.DATABASE
    user = settings_local.USER
    password = settings_local.PASSWORD
    host = settings_local.HOST
except:
    database = os.environ['DATABASE']
    user = os.environ['USER']
    password = os.environ['PASSWORD']
    host = os.environ['HOST']

db = PostgresqlDatabase(
    database=database,
    user=user,
    password=password,
    host=host,
    port=5432
)
