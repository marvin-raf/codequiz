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


def using_full_name_format(sheet):
    """
    Validates the contents of the headers in the excel doc and returns if the teacher
    is using full name format or given and last name format
    """

    if sheet.nrows == 0:
        raise ValueError("Wrong Format")

    # If there are only 2 columns in the first row, then just validate against {Email | Name}
    if len(sheet.row(0)) == 2:
        email = sheet.cell_value(rowx=0, colx=0)
        name = sheet.cell_value(rowx=0, colx=1)

        if email.lower() != "email" or name.lower() != "name":
            raise ValueError("Wrong Format")

        return True

    else:
        email = sheet.cell_value(rowx=0, colx=0)
        name_or_first_name = sheet.cell_value(rowx=0, colx=1)
        last_name = sheet.cell_value(rowx=0, colx=2)

        # Else, validate against both {Email | Name} and {Email | First Name | Last Name}
        if email.lower() != "email":
            raise ValueError("Wrong Format")

        if name_or_first_name.lower() == "first name":
            if last_name.lower() != "last name":
                raise ValueError("Wrong Format")

            return False
        elif name_or_first_name.lower() == "name":
            return True
        else:
            raise ValueError("Wrong format")


def parse_students(file_path):
    """
    Parses the email and names of students from the file_path excel doc
    """

    book = xlrd.open_workbook(file_path)

    sheet = book.sheet_by_index(0)

    student_list = []

    full_name_format = using_full_name_format(sheet)

    print(full_name_format)

    for i in range(1, sheet.nrows):
        if full_name_format:
            email = sheet.cell_value(rowx=i, colx=0)
            name = sheet.cell_value(rowx=i, colx=1)

            student_list.append({"name": name, "email": email})
        else:
            email = sheet.cell_value(rowx=i, colx=0)
            first_name = sheet.cell_value(rowx=i, colx=1)
            last_name = sheet.cell_value(rowx=i, colx=2)

            student_list.append({
                "name": "{} {}".format(first_name, last_name),
                "email": email
            })

    return student_list
