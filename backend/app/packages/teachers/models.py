"""
Contains models for the Teachers package
"""

import bcrypt
import pymysql
import uuid

from app.util import db


def create_hash(password):
    """
    Creates a hash out of the teachers password
    """
    teacher_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return teacher_hash


def taken_email(email):
    """
    Checks if the email is taken in the teacher or student table
    """

    query = """
    SELECT teacher_id FROM teachers
    WHERE teacher_email = %s
    """

    query2 = """
    SELECT student_id FROM students 
    WHERE student_email = %s
    """

    taken = db.query(query, (email))
    taken2 = db.query(query2, (email))
    return taken or taken2


def insert_teacher(name, email, teacher_hash):
    """
    Inserts a new teacher into the database
    """

    query = """
    INSERT INTO teachers (teacher_name, teacher_email, teacher_hash)
    VALUES (%s, %s, %s)
    """

    teacher_id = db.insert_query(query, (name, email, teacher_hash))
    return teacher_id
