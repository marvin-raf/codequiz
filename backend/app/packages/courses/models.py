"""
Contains models for the Courses package
"""

from app.util import db


def insert_course(name, teacher_id):
    """
    Inserts a course and returns its id
    """
    query = """
    INSERT INTO courses (course_name, course_teacher_id)
    VALUES (%s, %s)
    """
    course_id = db.insert_query(query, (name, teacher_id))
    return course_id