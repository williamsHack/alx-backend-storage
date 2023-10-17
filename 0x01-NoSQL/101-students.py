#!/usr/bin/env python3

"""
Write a Python function that returns all students sorted by average score:
Prototype: def top_students(mongo_collection):
mongo_collection will be the pymongo collection object
The top must be ordered
The average score must be part of each item returns with key = averageScore

"""

from pymongo import MongoClient

def top_students(mongo_collection):
    # Retrieve all students and calculate their average scores
    pipeline = [
        {"$project": {"name": 1, "scores": 1, "averageScore": {"$avg": "$scores.score"}}},
        {"$sort": {"averageScore": -1}}
    ]
    students = mongo_collection.aggregate(pipeline)

    return list(students)


"""
// run main function here

# Example usage
client = MongoClient('mongodb://localhost:27017')
db = client['your_database_name']
collection = db['your_collection_name']

top_students_list = top_students(collection)
for student in top_students_list:
    print(student)

client.close()

"""

