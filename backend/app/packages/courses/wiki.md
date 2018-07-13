# Courses Enpoints

[Back to main wiki](../../../wiki.md)

- ["/courses"](#markdown-header-courses)
- ["/courses/<id>"](#markdown-header-courses-id)
- ["/courses/<id>/quizzes"](#markdown-header-courses-id-quizzes)
- ["/courses/<id>/classes"](#markdown-header-courses-id-classes)
- ["/courses/<id>/classes/<id>"](#markdown-header-courses-id-classes-id)

## `courses`

### GET

**URL** `/courses`

**Description** This endpoint gets all of a teachers courses

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the courses have been successfully retrieved

    {
        "courses": [
            {
                "course_id": 1,
                "course_name": "string"
            }
        ]
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

### POST

**URL** `/courses`

**Description** This endpoint creates a course

**Authentication** Teacher

**Request Body**

    {
        "name": "string",
    }

**Responses**
Status Code (201)

Created response indicates the course has been created

    {
        "course_id": 1
    }

---

Status Code (400)

Bad Request indicates that

- `name` does not exist in request body
- `name` is empty

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `courses id`

### GET

**URL** `/courses/<id>`

**Description** This endpoint gets information about a course

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the quizzes have been successfully retrieved

    {
        "course_id": 1,
        "course_name": "string",
        "course_quizzes": [
            {
                "quiz_id": 1,
                "quiz_name": "string",
                "quiz_start_date": 1,
                "quiz_end_date": 1
            }
        ],
        "course_classes": [
            {
                "class_id": 1,
                "class_name": "string"
            }
        ]
    }

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `course_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `course_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

### PATCH

**URL** `/courses/<id>`

**Description** This endpoint changes name of a course

**Authentication** Teacher

**Request Body**

    {
        "name": "string"
    }

**Responses**
Status Code (200)

Success response indicates the course name has been changed

---

Status Code (400)

Bad Request indicates that

- `name` does not exist in request body
- `name` is empty

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `course_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `course_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

### DELETE

**URL** `/courses/<id>`

**Description** This endpoint deletes a course

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the course has been deleted

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `course_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates that

- `course_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `courses id quizzes`

### POST

**URL** `/courses/<id>/quizzes`

**Description** This endpoint creates a quiz

**Authentication** Teacher

**Request Body**

    {

        "name": "string",
        "start_date": 1,
        "end_date": 1

    }

**Responses**
Status Code (201)

Created response indicates the quiz has been created

    {
        "quiz_id": 1
    }

---

Status Code (400)

Bad Request indicates that

- `name`, `start_date` or `end_date` do not exist in request body
- `start_date` is after `end_date` or the current date is after `start_date`

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `course_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates that

- `course_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `courses id classes`

### POST

**URL** `/courses/<id>/classes`

**Description** This endpoint adds a class to a course

**Authentication** Teacher

**Request Body**

    {

        "id": "string"

    }

**Responses**
Status Code (200)

Succcess response indicates the class has been added

---

Status Code (400)

Bad Request indicates that

- `id` is missing
- `id` is incorrect

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `course_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates that

- `course_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `courses id classes id`

### DELETE

**URL** `/courses/<id>/classes/<id>`

**Description** This endpoint deletes a class from a course

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Succcess response indicates the class has been deleted from the course

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `course_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates that

- `course_id` doesn't match with a class in the database
- `class_id` and `course_id` doesn't match in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
