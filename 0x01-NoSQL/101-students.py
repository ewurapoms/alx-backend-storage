#!/usr/bin/env python3
""" script that returns all students sorted by average score"""


def top_students(mongo_collection):
    """ displays student scores"""
    students = mongo_collection.find()
    sorted_s = sorted(students, key=lambda student: student['averageScore'],
                      reverse=True)
    return sorted_s
