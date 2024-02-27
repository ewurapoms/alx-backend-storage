#!/usr/bin/env python3
""" Module displays Nginx logs stored in MongoDB"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("localhost", 27017)
    collection = client.logs.nginx

    logged = collection.count_documents({})
    print(f"Total logs: {logged}")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"{method}: {count}")
    count_status = collection.count_documents({"method": "GET",
                                               "path": "/status"})

    print(f"GET /status: {count_status}")
