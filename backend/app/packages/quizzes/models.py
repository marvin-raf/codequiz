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
