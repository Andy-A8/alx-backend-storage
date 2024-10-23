#!/usr/bin/env python3
"""
    Write a Python function that returns all students sorted by average score

    Prototype: def top_students(mongo_collection):
    mongo_collection will be the pymongo collection object
    The top must be ordered
    The average score must be part of each item returns with key = averageScore
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: The pymongo collection object.

    Returns:
        A list of students with their average score, sorted by average score.
    """
    students = list(mongo_collection.find())

    for student in students:
        scores = [topic['score'] for topic in student.get('topics', [])]
        average_score = sum(scores) / len(scores) if scores else 0
        student['averageScore'] = average_score

    # Sort students by average score in descending order
    sorted_students = sorted(students, key=lambda x: x['averageScore'],
                             reverse=True)

    return sorted_students
