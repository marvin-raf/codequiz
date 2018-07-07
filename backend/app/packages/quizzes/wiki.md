# Quizzes Enpoints

- ["/quizzes"](#/quizzes)

## `/quizzes`

### POST

**URL** `/quizzes`

**Description** This endpoints creates a quiz

**Authentication** Teacher

**Request Body**

    {
        "course_id": 1,
        "name": "string",
        "start_date": 1,
        "end_date": 1

    }

**Responses**
Status Code (201)

Success response indicates the quiz has been created

    {
        "quiz_id": 1
    }

---

Status Code (400)

Bad Request indicates that

- `name`, `course_id`, `start_date` or `end_date` do not exist in request body
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
