# Quizzes Enpoints

[Back to main wiki](../../../wiki.md)

- ["/quizzes/free"](#markdown-header-quizzes-free)
- ["/quizzes/<id>"](#markdown-header-quizzes-id)
- ["/quizzes/<id>/questions"](#markdown-header-quizzes-id)
- ["/quizzes/<id>/questions/<id>"](#markdown-header-quizzes-id-questions)
- ["/quizzes/<id>/questions/<id>/precheck"](#markdown-header-quizzes-id-questions-id-precheck)
- ["/quizzes/<id>/questions/<id>/check"](#markdown-header-quizzes-id-questions-id-precheck)

## `quizzes free`

### GET

**URL** `/quizzies/free`

**Description** This endpoint gets all the free quizzes that are available to everyone

**Authentication** None

**Request Body**

**Responses**
Status Code (200)

Success response indicates free quizzes have been successfully retrieved.

    [
        {
        "language_name": "string",
        "quiz_id": 1,
        "quiz_name": "string",
        "quiz_short_desc": "string"
        },
        ...
    ]

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `quizzes id`

### GET

**URL** `/quizzies/<id>`

**Description** This endpoint gets quiz name, start and end dates and all questions

**Authentication** Teacher, Student or no authentication 

**Request Body**

**Responses**
Status Code (200)

Unauthenticated response

Success response indicates the quiz details have been successfully retrieved

   {
    "questions": [
        {
            "question_description": "string",
            "question_id": 1,
            "question_quiz_id": 1,
            "test_cases": [
                {
                    "test_expected": "Hello World!",
                    "test_id": 3,
                    "test_input": "print(hello_world())"
                }
            ]
        },
        ...
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
