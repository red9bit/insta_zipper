from pymongo import MongoClient


def connect_to_mongodb():
    from flask import current_app
    config = current_app.config

    client = MongoClient(config['MONGO_HOST'])
    if config['MONGO_USER'] and config['MONGO_PASS']:
        client[config['MONGO_DB']].authenticate(config['MONGO_USER'], config['MONGO_PASS'])
    db = client[config['MONGO_DB']]

    return client, db


def str_or_none_cast(x):
    return None if str(x) == '<null>' else str(x)
