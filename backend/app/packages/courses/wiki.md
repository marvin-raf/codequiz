# Courses Enpoints

- ["/courses"](#/courses)

## `/courses`

### POST

**URL** `/courses`

**Description** This endpoints creates a course

**Authentication** Teacher

**Request Body**

    {
        "name": "string",
    }

**Responses**
Status Code (201)

Success response indicates the course has been created

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
