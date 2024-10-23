#!/usr/bin/env python3
"""
    Write a Python script that provides some stats about Nginx logs stored
    in MongoDB:

    Database: logs
    Collection: nginx
    Display (same as the example):
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with the method = ["GET", "POST",
    "PUT", "PATCH", "DELETE"] in this order (see example below - warning:
    it’s a tabulation before each line)
    one line with the number of documents with:
    method=GET
    path=/status
"""


from pymongo import MongoClient


def nginx_log_stats():
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method})
                     for method in methods}

    get_status_count = collection.count_documents({"method": "GET", "path":
                                                   "/status"})

    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{get_status_count} status check")


if __name__ == "__main__":
    nginx_log_stats()
