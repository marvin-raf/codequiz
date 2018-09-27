"""
Middleware functions
"""
import time
from functools import wraps
from flask import request
from app.util import db
from app.util.responses import unauthorized, bad_request, not_found, forbidden


def student_signed_in(func):
    """
    Checks to see if the teacher is authenticated or not.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if not "Student-Authorization" in request.headers:
            return unauthorized()

        query = """
        SELECT student_id
        FROM students
        WHERE student_token = %s
        """

        rows = db.query(query, (request.headers["Student-Authorization"]))

        if not rows:
            return unauthorized()

        request.student_id = rows[0]["student_id"]
        return func(*args, **kwargs)

    return wrap


def signed_in_or_out(func):
    """
    Checks if a teacher or student is signed in or out and saves the student or
    teacher in context if they are signed in
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Checks if the user is signed in as either a student or a teacher
        """

        if "Teacher-Authorization" in request.headers:
            query = """
            SELECT teacher_id 
            FROM teachers 
            WHERE teacher_token = %s
            """

            rows = db.query(query, (request.headers["Teacher-Authorization"]))

            if rows:
                request.teacher_id = rows[0]["teacher_id"]

        elif "Student-Authorization" in request.headers:
            query = """
            SELECT student_id 
            FROM students 
            WHERE student_token = %s
            """

            rows = db.query(query, (request.headers["Student-Authorization"]))

            if rows:
                request.student_id = rows[0]["student_id"]

        # If no user is authenticated, then go to next middleware
        return func(*args, **kwargs)

    return wrap


def teacher_signed_in(func):
    """
    Checks to see if the teacher is authenticated or not.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if not "Teacher-Authorization" in request.headers:
            return unauthorized()

        query = """
        SELECT teacher_is_admin, teacher_id
        FROM teachers 
        WHERE teacher_token = %s
        """

        rows = db.query(query, (request.headers["Teacher-Authorization"]))

        if not rows:
            return unauthorized()

        if rows[0]["teacher_is_admin"]:
            request.teacher_is_admin = True

        print(rows)
        request.teacher_id = rows[0]["teacher_id"]
        return func(*args, **kwargs)

    return wrap


def class_exists(func):
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        teacher_id = request.teacher_id
        class_id = request.view_args["class_id"]

        query = """
        SELECT * FROM classes
        WHERE class_id = %s
        """

        classes = db.query(query, (class_id))

        if not classes:
            return not_found()

        query = """
        SELECT * FROM classes
        WHERE class_id = %s
        AND class_teacher_id = %s
        """

        classes = db.query(query, (class_id, teacher_id))

        if not classes:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def course_exists(func):
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        teacher_id = request.teacher_id
        course_id = request.view_args["course_id"]

        query = """
        SELECT * FROM courses
        WHERE course_id = %s
        """

        courses = db.query(query, (course_id))

        if not courses:
            return not_found()

        query = """
        SELECT * FROM courses
        WHERE course_id = %s
        AND course_teacher_id = %s
        """

        courses = db.query(query, (course_id, teacher_id))

        if not courses:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def teacher_student_logged_in(func):
    """
    Checks to see if a student or a teacher is signed in.
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """Used to figure out whether to return the function or json"""

        if "Teacher-Authorization" in request.headers:
            query = """
            SELECT teacher_id 
            FROM teachers 
            WHERE teacher_token = %s
            """

            rows = db.query(query, (request.headers["Teacher-Authorization"]))

            if not rows:
                return unauthorized()

            request.teacher_id = rows[0]["teacher_id"]
            return func(*args, **kwargs)
        elif "Student-Authorization" in request.headers:
            query = """
            SELECT student_id
            FROM students
            WHERE student_token = %s
            """

            rows = db.query(query, (request.headers["Student-Authorization"]))

            if not rows:
                return unauthorized()

            request.student_id = rows[0]["student_id"]
            return func(*args, **kwargs)
        else:
            return unauthorized()

    return wrap


def teacher_owns_quiz(func):
    """
    Decorator
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        """
        Checks to see if teacher actually owns the quiz, or if 
        a teacher is an admin and the quiz is a free quiz
        """

        quiz_id = request.view_args["quiz_id"]

        query = """
        SELECT quiz_course_id
        FROM quizzes
        WHERE quiz_id = %s
        """

        quizzes = db.query(query, (quiz_id))

        # Checks if the quiz does not exist
        if not quizzes:
            return not_found()

        #If the course_id is null, check if teacher is an admin (Passed down from teacher_signed_in middleware)
        if quizzes[0]["quiz_course_id"] == None and hasattr(
                request, "teacher_is_admin"):
            return func(*args, **kwargs)

        # Check that teacher owns the course
        query = """
        SELECT quiz_id
        FROM quizzes
        INNER JOIN courses ON quizzes.quiz_course_id = courses.course_id
        INNER JOIN teachers ON courses.course_teacher_id = teachers.teacher_id
        WHERE quizzes.quiz_id = %s
        AND teachers.teacher_id = %s
        """

        quizzes = db.query(query, (quiz_id, request.teacher_id))

        if not quizzes:
            return forbidden()
        return func(*args, **kwargs)

    return wrap


def can_access_quiz(func):
    """Decorator"""

    @wraps(func)
    def wrap(*args, **kwargs):
        """Checks to see if either a teacher, student or unauthorized user
        can access the quiz

           If a student is logged in, check whether their teacher owns the quiz
           If a teacher is logged in, wheck whether they own the course for that quiz
        """
        quiz_id = request.view_args["quiz_id"]

        # Check that the quiz exists
        query = """
        SELECT quiz_id, quiz_course_id, quiz_start_date * 1000 AS quiz_start_date
        FROM quizzes
        WHERE quiz_id = %s
        """

        quizzes = db.query(query, (quiz_id))

        if not quizzes:
            return not_found()

        # IMPORTANT: If the course_id is null for the quiz, that means anyone can view the quiz
        if not quizzes[0]["quiz_course_id"]:
            return func(*args, **kwargs)

        if hasattr(request, "teacher_id"):
            teacher_id = request.teacher_id

            # Check that teacher owns the course
            query = """
            SELECT quiz_id 
            FROM quizzes
            INNER JOIN courses ON quizzes.quiz_course_id = courses.course_id
            INNER JOIN teachers ON courses.course_teacher_id = teachers.teacher_id
            WHERE quizzes.quiz_id = %s
            AND teachers.teacher_id = %s
            """

            quizzes = db.query(query, (quiz_id, teacher_id))

            if not quizzes:
                return forbidden()
            return func(*args, **kwargs)
        elif hasattr(request, "student_id"):
            student_id = request.student_id

            quiz_id = request.view_args["quiz_id"]

            # If the quiz hasn't started yet, then don't let student access
            current_time = int(time.time() * 1000)

            if current_time < quizzes[0]["quiz_start_date"]:
                return forbidden()

            # Check that students teacher owns the quiz
            query = """
            SELECT students_classes.sc_student_id
            FROM quizzes
            INNER JOIN classes_courses ON quizzes.quiz_course_id = classes_courses.cc_course_id
            INNER JOIN courses ON classes_courses.cc_course_id = courses.course_id
            INNER JOIN students_classes ON classes_courses.cc_class_id = students_classes.sc_class_id
            WHERE students_classes.sc_student_id = %s AND quiz_id = %s
            """

            rows = db.query(query, (student_id, quiz_id))

            if not rows:
                return forbidden()

            return func(*args, **kwargs)

        return unauthorized()

    return wrap


def question_exists(func):
    """
    Check that a question exists in a quiz
    """

    @wraps(func)
    def wrap(*args, **kwargs):

        quiz_id = request.view_args["quiz_id"]
        question_id = request.view_args["question_id"]

        query = """
        SELECT question_id
        FROM questions
        WHERE question_quiz_id = %s AND question_id = %s
        """
        rows = db.query(query, (quiz_id, question_id))

        if not rows:
            return forbidden()

        return func(*args, **kwargs)

    return wrap


def test_case_exists(func):
    """
    Checks that a test case exists in a question 
    """

    @wraps(func)
    def wrap(*args, **kwargs):
        test_id = request.view_args["test_id"]
        question_id = request.view_args["question_id"]

        query = """
        SELECT test_id
        FROM tests
        WHERE test_id = %s AND test_question_id = %s
        """

        test_cases = db.query(query, (test_id, question_id))

        if not test_cases:
            return forbidden()
        return func(*args, **kwargs)

    return wrap
