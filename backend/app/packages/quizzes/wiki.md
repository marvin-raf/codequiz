# Quizzes Enpoints

[Back to main wiki](../../../wiki.md)

- ["/quizzes/<id>"](#markdown-header-quizzes-id)
- ["/courses/<id>/questions"](#markdown-header-quizzes-id-questions)

## `quizzes id`

### GET

**URL** `/quizzies/<id>`

**Description** This endpoint gets quiz name, start and end dates and all questions

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the quiz have been successfully retrieved

    {
        "questions": [
            {
                "question_description": "string",
                "question_id": 1,
                "question_quiz_id": 1,
                "test_cases": [
                    {
                        "test_expected": "string",
                        "test_id": 1,
                        "test_input": "string"
                    }
                ]
            },
        ],
        "quiz": {
            "quiz_course_id": 1,
            "quiz_end_date": 1,
            "quiz_id": 1,
            "quiz_name": "string",
            "quiz_start_date": 1
        }
    }

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `quizzes id questions`

### POST

**URL** `/quizzies/<id>/questions`

**Description** This endpoint adds one question to the quiz

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (201)

Created response indicates that the question has been successfully added to the quiz

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
