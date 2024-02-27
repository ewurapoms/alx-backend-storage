#!/usr/bin/env python3
""" script that returns all students sorted by average score"""

def top_students(mongo_collection):
    """ displays student scores"""
    return mongo_collection.aggregate([
        {
            "$project":
                {
                    "name": "$name",
                    "averageScore": {"$avg": "$topics.score"}
                }
        },
        {
            "$sort":
                {
                    "averageScore": -1
                }
        }
    ])
