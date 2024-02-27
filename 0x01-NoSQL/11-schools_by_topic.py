#!/usr/bin/env python3
""" Module finds school by topic"""

import pymongo


def schools_by_topic(mongo_collection, topic):
    """displays a list of school with specific topic """

    return mongo_collection.find({"topics": topic})
