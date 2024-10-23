#!/usr/bin/env python3
"""
    Improve 12-log_stats.py by adding the top 10 of the most present
    IPs in the collection nginx of the database logs:

    The IPs top must be sorted
"""


from pymongo import MongoClient


def get_nginx_stats():
    # Connect to the MongoDB database
    client = MongoClient('mongodb://localhost:27017/')
    db = client['logs']
    collection = db['nginx']

    total_logs = collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents({"method": method})
                     for method in methods}

    get_status_count = collection.count_documents({"method": "GET", "path":
                                                   "/status"})

    ip_pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ]
    top_ips = list(collection.aggregate(ip_pipeline))

    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"    method {method}: {method_counts[method]}")
    print(f"{get_status_count} status check")

    print("Top 10 IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    get_nginx_stats()
