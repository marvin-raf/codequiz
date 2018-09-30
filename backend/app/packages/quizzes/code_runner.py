"""
Class that contains everything to do with running students code
"""

import os
from app.util import db
import subprocess

RUN_CODE_FILE = os.path.join("app", "packages", "quizzes", "run_code.sh")
RUN_CODE_COMMAND = "bash " + RUN_CODE_FILE + " {}"
TIME_LIMIT_EXCEEDED = "ERROR: Time Limit Exceeded"


class Test:
    def __init__(self, test_id, test_input, test_expected):
        self.test_id = test_id
        self.test_input = test_input
        self.test_expected = test_expected

    def has_test_input(self):
        """
        Checks if the test case has an input 
        """
        return self.test_input


class CodeRunner:
    """
    Everything to do with running students code
    """

    def __init__(self, student_id, quiz_id, question_id):
        # Map List of test_case dictionary to list of objects
        self.test_cases = None

        filename = "code_{}_{}_{}.py".format(student_id, quiz_id, question_id)

        self.filepath = os.path.join("app", "packages", "quizzes",
                                     "question_files", filename)
        # student_id will be a UUID if the user is not a student
        self.student_id = student_id
        self.question_id = question_id
        self.quiz_id = quiz_id

    def run_code(self, filepath):
        """
        This function is responsible for running code and returning STDOUT or an error

        Returns a tuple in form (output, is_error). Errors can either be incorrect tests
        or 
        """
        bashCommand = RUN_CODE_COMMAND.format(filepath)
        try:
            output = subprocess.check_output(
                bashCommand.split(), stderr=subprocess.STDOUT, timeout=5)

            print(output)
        # Gets called if python program returns an error code
        except subprocess.CalledProcessError as e:
            return "\n".join(e.output.decode().split("\n")[1:]), True

        # Gets called if timeout expires
        except subprocess.TimeoutExpired as e:
            return TIME_LIMIT_EXCEEDED, True

        return output.decode(), False

    def write_code(self, code):
        """
        Writes the code to a file with the format code_{student_id}_{quiz_id}_{question_id}.py
        """

        with open(self.filepath, "w") as f:
            f.write(code)

    def remove_code(self):
        """
        Removes students code
        """
        os.remove(self.filepath)

    def run(self, test_cases):
        """
        Takes an array of tests, runs them against students code
        and returns the output
        """

        results = []

        # Remap list of dictionaries to list of Test objects
        test_cases = list(
            map(lambda test: Test(test["test_id"], test["test_input"], test["test_expected"]),
                test_cases))

        question_is_wrong = False

        for test_case in test_cases:
            if not test_case.has_test_input():
                result = self.run_test_no_input()
            else:
                result = self.run_test_with_input(test_case)

            result["test_id"] = test_case.test_id
            result["test_input"] = test_case.test_input
            result["test_expected"] = test_case.test_expected

            if result["output"] != result["test_expected"]:
                question_is_wrong = True

            results.append(result)

        # Also returns question_worth total_negated and last_attempt_wrong to stay consistent
        return results, 0 if question_is_wrong else 10, 10 if question_is_wrong else 0, question_is_wrong

    def run_test_no_input(self):
        """
        Runs a test case which does not contains test input (e.g. Program code)
        """
        test_case = {}

        output, is_error = self.run_code(self.filepath)
        test_case["output"] = output
        test_case["error"] = is_error

        return test_case

    def run_test_with_input(self, test_case):
        """
        Runs a test case which contains a test input (e.g. Function Code)
        """

        test_case_result = {}

        test_filepath = os.path.join("app", "packages", "quizzes",
                                     "question_files",
                                     "test_case_{}_{}.py".format(
                                         test_case.test_id, self.student_id))

        with open(test_filepath, "w") as f:
            f.write("from code_{}_{}_{} import *\n".format(
                self.student_id, self.quiz_id, self.question_id))
            f.write(test_case.test_input)

        output, is_error = self.run_code(test_filepath)
        os.remove(test_filepath)

        test_case_result["output"] = output.strip()
        test_case_result["error"] = is_error

        return test_case_result
