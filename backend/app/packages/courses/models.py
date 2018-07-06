"""
Contains models for the Courses package
"""
from app.util import db


def insert_course(teacher_id, name):
    """
    Inserts a course and returns its id
    """
    query = """
    INSERT INTO courses (course_teacher_id, course_name)
    VALUES (%s, %s)
    """
    course_id = db.insert_query(query, (teacher_id, name))
    return course_id