from pymongo import MongoClient
from flask import current_app


def get_users_collection():
    client = MongoClient(current_app.config['MONGO_URI'])
    db = client[current_app.config['MONGO_DB']]
    return db[current_app.config['MONGO_COL']]