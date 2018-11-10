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


def get_class(class_id):
    """
    Gets class details based on the class_id
    """

    query = """
    SELECT class_id, class_name 
    FROM classes
    WHERE class_id = %s
    """

    classes = db.query(query, (class_id))

    return classes[0]


def get_students(class_id):
    """
    Gets all the students of a class
    """

    query = """
    SELECT 
    students.student_id AS student_id, 
    students.student_name AS student_name, 
    students.student_email AS student_email,
    IF(students.student_hash IS NOT NULL and students.student_hash != '', True, False) AS student_activated
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
    INSERT INTO students 
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

    query = query[:-2]  # Delete last trailing comma

    db.query(query, tuple(values))
    return


def delete_unique():
    """
    Deletes student emails that are already taken by a teacher
    """

    query = """
    DELETE FROM students
    WHERE student_email IN 
    (SELECT teacher_email FROM teachers)
    """

    db.query(query)
    return


def insert_into_class(class_id, emails):
    """
    Adds students into students_classes
    """

    query = """
    INSERT IGNORE INTO students_classes (sc_student_id, sc_class_id)
    SELECT student_id, %s
    FROM students
    WHERE student_email IN %s
    """

    db.query(query, (class_id, emails))


def delete_students(class_id):
    """
    Deletes all students in a class
    """

    query = """
    DELETE FROM students_classes
    WHERE sc_class_id = %s
    """

    db.query(query, (class_id))
    return


def check_student(class_id, student_id):
    """
    Checks if a student exists or if he matches a class
    """

    query = """
    SELECT * FROM students_classes
    WHERE sc_class_id = %s
    AND sc_student_id = %s
    """

    student = db.query(query, (class_id, student_id))

    return student


def check_email(email):
    """
    Checks to see if a students email is taken
    """

    query = """
    SELECT student_id
    FROM students
    WHERE student_email = %s
    """

    query2 = """
    SELECT teacher_id 
    FROM teachers
    WHERE teacher_email = %s
    """

    students = db.query(query, (email))
    teachers = db.query(query2, (email))

    return True if students or teachers else False


def delete_student(student_id):
    """
    Deletes a student
    """

    query = """
    DELETE FROM students
    WHERE student_id = %s
    """

    db.query(query, (student_id))