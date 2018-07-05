"""
Contains models for the Teachers package
"""

import bcrypt
import pymysql
from app.util import db


def create_hash(password):
    """
    Creates a hash out of the teachers password
    """
    teacher_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return teacher_hash


def taken_email(email):
    """
    Checks if the email is taken
    """
    query = """
    SELECT teacher_id FROM teachers
    WHERE teacher_email = %s
    """
    taken = db.query(query, (email))
    return taken


def insert_teacher(name, email, teacher_hash):
    """
    Inserts a new teacher into the database
    """
    query = """
    INSERT INTO teachers (teacher_name, teacher_email, teacher_hash)
    VALUES (%s, %s, %s);
    SELECT LAST_INSERT_ID()
    """
    teacher_id = db.query(query, (name, email, teacher_hash))
    return teacher_id
