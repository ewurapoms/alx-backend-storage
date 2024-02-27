#!/usr/bin/env python3
""" Module displays Nginx logs stored in MongoDB"""

from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient("localhost", 27017)
    collection = client.logs.nginx

    update = collection.count_documents({})
    print(f"{update} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        output = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {output}")
    final_count = collection.count_documents({"method": "GET",
                                              "path": "/status"})
    print(f"{final_count} log check")
