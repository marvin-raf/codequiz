"""
Contains models for the Classes package
"""
from app.util import db


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


def class_exists(class_id, teacher_id):
    """
    Checks if the class_id supplied exists
    """

    query = """
    SELECT * FROM classes
    WHERE class_id = %s
    AND class_teacher_id = %s
    """

    classes = db.query(query, (class_id, teacher_id))
    return classes


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