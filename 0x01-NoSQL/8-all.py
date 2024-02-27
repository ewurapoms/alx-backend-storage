#!/usr/bin/env python3
""" Module that lists all document """

import pymongo


def list_all(mongo_collection):
    """
    Lists all documents in a collection
    Return an empty list if no document in the collection
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
