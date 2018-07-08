# Courses Enpoints

- ["/courses"](#/courses)
- ["/courses/<id>"](#/courses/<id>)
- ["/courses/<id>/quizzes"](#/courses/<id>/quizzes)

## `/courses`

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

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

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

---

Status Code (401)

Unauthorized indicates that

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `/courses/<id>`

### GET

**URL** `/courses/<id>`

**Description** This endpoint gets information about a course

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the quizzes have been successfully retrieved

    {
        "quizzes": [
            {
                "quiz_id": 1,
                "quiz_name": "string",
                "quiz_start_date": 1,
                "quiz_end_date": 1
            }
        ]
    }

---

Status Code (400)

Bad request indicates that

- `course_id` does not exist in course table
- `course_id` is not assigned to the authenticated teacher

---

Status Code (401)

Unauthorized indicates that

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `/courses/<id>/quizzes`

### GET

**URL** `/courses/<id>/quizzes`

**Description** This endpoint gets all quizzes from a course

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the quizzes have been successfully retrieved

    {
        "quizzes": [
            {
                "quiz_id": 1,
                "quiz_name": "string",
                "quiz_start_date": 1,
                "quiz_end_date": 1
            }
        ]
    }

---

Status Code (400)

Bad request indicates that

- `course_id` does not exist in course table
- `course_id` is not assigned to the authenticated teacher

---

Status Code (401)

Unauthorized indicates that

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

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
- `course_id` does not exist in course table
- `course_id` is not assigned to the authenticated teacher
- `start_date` is after `end_date` or the current date is after `start_date`

---

Status Code (401)

Unauthorized indicates that

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
