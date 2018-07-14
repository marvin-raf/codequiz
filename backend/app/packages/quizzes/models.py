"""
Contains models for the Quizzes package
"""
from app.util import db


def get_name(quiz_id):
    """
    Gets name of a quiz based on the quiz_id
    """

    query = """
    SELECT quiz_name 
    FROM quizzes 
    WHERE quiz_id = %s
    """

    quizzes = db.query(query, (quiz_id))

    return quizzes[0]["quiz_name"]


def get_questions(quiz_id):
    """
    Gets questions based on quiz id
    """

    query = """
    SELECT *
    FROM questions
    WHERE question_quiz_id = %s
    ORDER BY question_id
    """

    questions = db.query(query, (quiz_id))

    return questions


def get_tests(questions):
    """
    Gets question test cases based on quiz id
    """

    for question in questions:
        query = """
        SELECT test_id, test_input, test_expected
        FROM tests
        WHERE test_question_id = %s
        """

        test_cases = db.query(query, (question["question_id"]))
        question["test_cases"] = test_cases

    return questions
