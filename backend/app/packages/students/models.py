"""
Contains models for the Students package
"""

import bcrypt
import pymysql
from app.util import db


def create_hash(student_password):
    """
    Creates a hash out of the students password
    """

    student_hash = bcrypt.hashpw(student_password.encode(), bcrypt.gensalt())
    return student_hash


def save_hash(student_hash, student_activate_token):
    """
    Saves the students hash in the db
    """

    query = """
    UPDATE students 
    SET student_hash = %s
    WHERE student_token = %s
    """
    db.query(query, (student_hash, student_activate_token))


def token_exists(student_token):
    """
    Checks if token exists in students table
    """

    query = """
    SELECT student_token
    FROM students
    WHERE student_activate_token = %s
    """

    rows = db.query(query, (student_token))

    if rows:
        return True

    return False


def id_from_credentials(student_email, student_password):
    """
    Gets the students_id from their credentials. If their credentials
    don't match, then None will be returned
    """

    query = """
    SELECT student_id, student_hash
    FROM students
    WHERE student_email = %s
    """

    rows = db.query(query, (student_email))

    if not rows:
        return None

    student_hash = rows[0]["student_hash"]
    student_id = rows[0]["student_id"]

    # Compared hashed password from request to hashed password in db
    if bcrypt.hashpw(student_password, student_hash) == student_hash:
        return student_id

    return None


def create_token():
    """
    Creates the students login token
    """
    pass


def save_token(student_token, student_id):
    """
    Saves the student token
    """

    query = """
    UPDATE students
    SET student_token = %s
    WHERE student_id = %s
    """

    db.query(query, (student_token, student_id))
