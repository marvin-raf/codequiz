"""
Contains models for the Courses package
"""
from app.util import db
import time


def get_courses(teacher_id):
    """
    Gets all of a teachers courses
    """

    query = """
    SELECT course_id, course_name
    FROM courses
    WHERE course_teacher_id = %s
    """

    courses = db.query(query, (teacher_id))
    return courses


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
    return course


def get_course(course_id):
    """
    Gets information on one course
    """

    query = """
    SELECT * FROM courses
    WHERE course_id = %s
    """

    course = db.query(query, (course_id))
    return course


def get_quizzes(course_id):
    """
    Gets all of a courses quizzes
    """

    query = """
    SELECT quiz_id, quiz_name, quiz_start_date, quiz_end_date
    FROM quizzes
    WHERE quiz_course_id = %s
    """

    quizzes = db.query(query, (course_id))
    return quizzes


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