#!/usr/bin/env python3
"""Module that inserts documents into school with kwargs"""


from pymongo import MongoClient


client = MongoClient("localhost", 27017)
collection = client.my_db.mongo_collection


def insert_school(mongo_collection, **kwargs):
    """ Inserts into school collection """
    return mongo_collection.insert_one(kwargs).inserted_id


client.close()
