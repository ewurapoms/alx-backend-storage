#!/usr/bin/env python3
""" Module adds top 10 IPs to Nginx logs stored in MongoDB"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient("localhost", 27017)
    collection = client.logs.nginx

    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        result = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {result}")
    status_check_count = collection.count_documents({"method": "GET",
                                                     "path": "/status"})
    print(f"{status_check_count} status check")
    top_ips = collection.aggregate([
        {
            "$group": {
                "_id": "$ip",
                "count": {
                    "$sum": 1
                }
            }
        },
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")
