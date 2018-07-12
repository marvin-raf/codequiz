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


def get_name(course_id):
    """
    Gets information on one course
    """

    query = """
    SELECT course_name FROM courses
    WHERE course_id = %s
    """

    course = db.query(query, (course_id))
    return course[0]["course_name"]


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


def get_classes(course_id):
    """
    Gets all of a courses classes
    """

    query = """
    SELECT 
    classes.class_id AS class_id,
    classes.class_name AS class_name
    FROM classes 
    INNER JOIN classes_courses
    ON classes.class_id = classes_courses.cc_class_id
    WHERE cc_course_id = %s
    """

    classes = db.query(query, (course_id))
    return classes


def change_course(course_id, name):
    """
    Changes the name of a course
    """

    query = """
    UPDATE courses
    SET course_name = %s
    WHERE course_id = %s
    """

    db.query(query, (name, course_id))
    return


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