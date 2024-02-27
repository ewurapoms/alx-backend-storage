#!/usr/bin/env python3
""" Module displays Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def top_ips(collection):
    pipeline = [
        {"$group": {"_id": "$remote_addr", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = collection.aggregate(pipeline)
    return list(top_ips)


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

    top_ips_list = top_ips(collection)
    print("Top 10 IPs:")
    for idx, ip_data in enumerate(top_ips_list, 1):
        print(f"\t{idx}. IP: {ip_data['_id']}, Count: {ip_data['count']}")
