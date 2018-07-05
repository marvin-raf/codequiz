"""
Contains models for the Students package
"""

import bcrypt
import pymysql
import uuid

from app.util import db


def create_hash(password):
    """
    Creates a hash out of the students password
    """

    student_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return student_hash


def save_hash(student_hash, activate_token):
    """
    Saves the students hash in the db
    """

    query = """
    UPDATE students 
    SET student_hash = %s
    WHERE student_token = %s
    """
    db.query(query, (student_hash, activate_token))


def token_exists(token):
    """
    Checks if token exists in students table
    """

    query = """
    SELECT student_token
    FROM students
    WHERE student_activate_token = %s
    """

    rows = db.query(query, (token))

    if rows:
        return True

    return False


def id_from_credentials(email, password):
    """
    Gets the students_id from their credentials. If their credentials
    don't match, then None will be returned
    """

    query = """
    SELECT student_id, student_hash
    FROM students
    WHERE student_email = %s
    """

    rows = db.query(query, (email))

    if not rows:
        return None

    student_hash = rows[0]["student_hash"]
    student_id = rows[0]["student_id"]

    # Compared hashed password from request to hashed password in db
    if bcrypt.hashpw(password, student_hash) == student_hash:
        return student_id

    return None


def create_token():
    """
    Creates the students login token
    """

    token = uuid.uuid4().hex

    query = """
    SELECT student_token
    FROM students
    WHERE student_token = %s
    """

    rows = db.query(query, (token))

    if rows:
        return create_token()

    return token


def save_token(token, student_id):
    """
    Saves the student token
    """

    query = """
    UPDATE students
    SET student_token = %s
    WHERE student_id = %s
    """

    db.query(query, (token, student_id))
