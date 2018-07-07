"""
Contains models for the Students package
"""

import os
import bcrypt
import pymysql
import uuid
import xlrd
from config import config

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
    WHERE student_activate_token = %s
    """

    db.query(query, (student_hash, activate_token))


def token_exists(token):
    """
    Checks if token exists in students table
    """

    query = """
    SELECT student_activate_token
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
    WHERE student_email = %s AND student_hash IS NOT NULL
    """

    rows = db.query(query, (email))

    if not rows:
        return None

    student_hash = rows[0]["student_hash"]
    student_id = rows[0]["student_id"]

    # Compared hashed password from request to hashed password in db
    if bcrypt.hashpw(password.encode(),
                     student_hash.encode()) == student_hash.encode():
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


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ["xlsx", "xlsm"]


def save_excel_doc(excel_doc):
    """
    Saves the excel doc in the config["UPLOAD_FOLDER"] directory
    """

    filename = "{}.xlsx".format(uuid.uuid4())
    file_path = os.path.join(config["UPLOAD_FOLDER"], filename)
    excel_doc.save(file_path)

    return file_path


def parse_students(file_path):
    """
    Parses the email and names of students from the file_path excel doc
    """

    book = xlrd.open_workbook(file_path)

    sheet = book.sheet_by_index(0)

    student_list = []

    for i in range(sheet.nrows):
        name_cell = sheet.cell_value(rowx=i, colx=0)
        email_cell = sheet.cell_value(rowx=i, colx=1)

        if i == 0:
            if name_cell.lower() != "name" or email_cell.lower() != "email":
                raise ValueError("Name or Email header is wrong")
        else:
            student_list.append({"name": name_cell, "email": email_cell})

    return student_list
