"""
Contains models for the Classes package
"""
from app.util import db
import uuid


def get_classes(teacher_id):
    """
    Gets all of a teachers classes
    """

    query = """
    SELECT class_id, class_name
    FROM classes
    WHERE class_teacher_id = %s
    """

    classes = db.query(query, (teacher_id))
    return classes


def insert_class(teacher_id, name):
    """
    Inserts a class and returns its id
    """

    query = """
    INSERT INTO classes (class_teacher_id, class_name)
    VALUES (%s, %s)
    """

    class_id = db.insert_query(query, (teacher_id, name))
    return class_id


def change_class(class_id, name):
    """
    Changes the information of a class
    """

    query = """
    UPDATE classes
    SET class_name = %s
    WHERE class_id = %s
    """

    db.query(query, (name, class_id))
    return


def delete_class(class_id):
    """
    Deletes a class
    """

    query = """
    DELETE FROM classes
    WHERE class_id = %s
    """

    db.query(query, (class_id))
    return


def get_students(class_id):
    """
    Gets all the students of a class
    """

    query = """
    SELECT 
    students_classes.sc_student_id AS student_id, 
    students.student_name AS student_name, 
    students.student_email AS student_email
    FROM students_classes 
    INNER JOIN students ON students_classes.sc_student_id = students.student_id
    WHERE students_classes.sc_class_id = %s
    """

    students = db.query(query, (class_id))
    return students


def insert_students(students, teacher_id):
    """
    Inserts a list of students into database
    """

    query = """
    INSERT IGNORE INTO students 
    (student_teacher_id, student_name, student_email, student_activate_token)
    VALUES
    """
    values = []
    token = None
    for student in students:
        token = uuid.uuid4().hex
        query += "(%s, %s, %s, %s), "
        values.append(teacher_id)
        values.append(student["name"])
        values.append(student["email"])
        values.append(token)

    query = query[:-2]

    student_list = db.query(query, tuple(values))
    return student_list
