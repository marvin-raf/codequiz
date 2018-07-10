import uuid
import bcrypt

from app.util import db


def id_from_credentials(email, password):
    """
    Gets the teacher_id or student-id from their credentials. If their credentials
    don't match, then None will be returned
    """

    query = """
    SELECT teacher_id, teacher_hash
    FROM teachers
    WHERE teacher_email = %s
    """

    rows = db.query(query, (email))

    if rows:
        teacher_hash = rows[0]["teacher_hash"]
        teacher_id = rows[0]["teacher_id"]

        # Compared hashed password from request to hashed password in db
        if bcrypt.hashpw(password.encode(),
                         teacher_hash.encode()) == teacher_hash.encode():
            return teacher_id, True

    else:
        query = """
        SELECT student_id, student_hash 
        FROM students 
        WHERE student_email = %s
        """

        rows = db.query(query, (email))

        if rows:
            student_hash = rows[0]["student_hash"]
            student_id = rows[0]["student_id"]

            # Compared hashed password from request to hashed password in db
            if bcrypt.hashpw(password.encode(),
                             student_hash.encode()) == student_hash.encode():
                return student_id, False

    return None, None


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

    query2 = """
    SELECT student_token
    FROM students
    WHERE student_token = %s
    """

    rows = db.query(query, (token))
    rows2 = db.query(query2, (token))

    if rows or rows2:
        return create_token()

    return token


def save_token(token, user_id, is_teacher):
    """
    Saves the teachers or students token
    """

    if is_teacher:
        query = """
        UPDATE teachers
        SET teacher_token = %s
        WHERE teacher_id = %s
        """
    else:
        query = """
        UPDATE students 
        SET student_token = %s
        WHERE student_id = %s
        """

    db.query(query, (token, user_id))


def remove_token(user_id, is_teacher):
    """
    Sets a teachers or students token to null in the database
    """

    if is_teacher:
        query = """
        UPDATE teachers
        SET teacher_token = %s
        WHERE teacher_id = %s
        """
    else:
        query = """
        UPDATE teachers
        SET student_token = %s
        WHERE student_id = %s
        """

    db.query(query, (None, user_id))
