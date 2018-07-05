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


def id_from_credentials(email, password):
    """
    Gets the teacher_id from their credentials. If their credentials
    don't match, then None will be returned
    """

    query = """
    SELECT teacher_id, teacher_hash
    FROM teachers
    WHERE teacher_email = %s
    """

    rows = db.query(query, (email))

    if not rows:
        return None

    teacher_hash = rows[0]["teacher_hash"]
    teacher_id = rows[0]["teacher_id"]

    # Compared hashed password from request to hashed password in db
    if bcrypt.hashpw(password.encode(),
                     teacher_hash.encode()) == teacher_hash.encode():
        return teacher_id

    return None


def create_token():
    """
    Creates the teachers login token
    """

    token = uuid.uuid4().hex

    query = """
    SELECT teacher_token
    FROM teachers
    WHERE teacher_token = %s
    """

    rows = db.query(query, (token))

    if rows:
        return create_token()

    return token


def save_token(token, teacher_id):
    """
    Saves the teachers token
    """

    query = """
    UPDATE teachers
    SET teacher_token = %s
    WHERE teacher_id = %s
    """

    db.query(query, (token, teacher_id))


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
    VALUES (%s, %s, %s)
    """

    teacher_id = db.insert_query(query, (name, email, teacher_hash))
    return teacher_id
