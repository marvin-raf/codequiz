"""
Contains models for the Quizzes package
"""
import os
from app.util import db
import subprocess

RUN_CODE_COMMAND = "python3 {}"


def get_quiz(quiz_id):
    """
    Gets name of a quiz based on the quiz_id
    """

    query = """
    SELECT *
    FROM quizzes 
    WHERE quiz_id = %s
    """

    quizzes = db.query(query, (quiz_id))

    return quizzes[0]


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


def get_tests(questions, student_id):
    """
    Gets question test cases based on quiz id
    """

    for question in questions:
        query = """
        SELECT test_id, test_input, test_expected
        FROM tests
        WHERE test_question_id = %s
        """

        query2 = """
        SELECT answers.answer_id, tests.test_input, tests.test_expected, answers.answer_content
FROM answers
INNER JOIN tests ON answers.answer_test_id = tests.test_id
WHERE answer_attempt_id = (SELECT attempt_id 
							FROM attempt
							WHERE attempt_student_id = %s
							AND attempt_question_id = %s
							ORDER BY attempt_id
							DESC LIMIT 1) 
AND answer_test_id IN (SELECT test_id
					   FROM tests
					   WHERE test_question_id = %s
					   )
        """

        test_cases = db.query(query, (question["question_id"]))

        test_case_results = db.query(
            query2, (student_id, question["question_id"], student_id))

        # Gets the latest test case results
        question["test_cases"] = test_cases
        question["test_case_results"] = test_case_results

    return questions


def add_question(quiz_id, description):
    """
    Adds a question to a quiz
    """

    query = """
    INSERT INTO questions (question_quiz_id, question_description)
    VALUES (%s, %s)
    """

    question_id = db.insert_query(query, (quiz_id, description))

    return question_id


def add_tests(question_id, test_cases):
    """
    Adds test cases for a specific problem
    """

    query = """
    INSERT INTO tests (test_question_id, test_input, test_expected)
    VALUES (%s, %s, %s)
    """
    tests = map(
        lambda test: (question_id, test["test_input"], test["test_expected"]),
        test_cases)

    db.insert_many(query, tuple(tests))


def precheck_file_name(student_id, quiz_id, question_id):
    return "code_{}_{}_{}.py".format(student_id, quiz_id, question_id)


def run_code(filepath):
    """
    Runs python code for a specific filetype and language

    Returns output and exit code
    """
    bashCommand = RUN_CODE_COMMAND.format(filepath)
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    is_error = process.wait()

    output, _ = process.communicate()

    return output, is_error


def get_test_cases(question_id):
    """
    Gets the test cases for a specific question in the quiz
    """

    query = """
    SELECT test_id, test_input, test_expected
    FROM tests 
    WHERE test_question_id = %s
    """

    test_cases = db.query(query, (question_id))

    return test_cases


def run_test_cases(test_cases, filepath, student_id, quiz_id, question_id,
                   code):
    """
    Runs test cases for a specific question in a quiz. 

    Returns the output of test cases
    """

    results = []

    for test_case in test_cases:
        if not test_case["test_input"]:
            output, is_error = run_code(filepath)
            test_case["output"] = output
            test_case["error"] = is_error
            results.append(test_case)
            break
        else:
            filepath = os.path.join("app", "packages", "quizzes",
                                    "question_files",
                                    "test_case_{}_{}.py".format(
                                        test_case["test_id"], student_id))

            with open(filepath, "w") as f:
                f.write("from code_{}_{}_{} import *\n".format(
                    student_id, quiz_id, question_id))
                f.write(code)
                f.write("\n")
                f.write(test_case["test_input"])

            output, is_error = run_code(filepath)
            test_case["output"] = output.strip()
            test_case["error"] = is_error

            results.append(test_case)

    return results


def insert_test_cases(test_case_results, student_id):
    """
    Inserts a users test cases into answers table 
    """
    query = """
    INSERT INTO answers
    VALUES (DEFAULT, %s, %s, %s)
    """

    for test_case in test_case_results:
        db.query(query,
                 (test_case["output"], student_id, test_case["test_id"]))
