"""
Contains models for the Quizzes package
"""
from app.util import db
import time


def course_exists(course_id, teacher_id):
    """
    Checks if the course_id supplied exists
    """
    query = """
    SELECT * FROM courses
    WHERE course_id = %s
    AND course_teacher_id = %s
    """

    course = db.query(query, (course_id, teacher_id))
    print(course)
    print(course)
    return course


def check_dates(start_date, end_date):
    """
    Returns true if dates are in the right order
    """
    current_date = int(time.time())
    if current_date <= start_date and start_date <= end_date:
        return True
    return False


def insert_quiz(course_id, name, start_date, end_date):
    """
    Inserts a quiz and returns its id
    """
    query = """
    INSERT INTO quizzes (quiz_course_id, quiz_name, quiz_start_date, quiz_end_date)
    VALUES (%s, %s, %s, %s)
    """
    quiz_id = db.insert_query(query, (course_id, name, start_date, end_date))
    return quiz_id
