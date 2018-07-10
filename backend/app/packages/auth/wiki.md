## signin

**URL** `/auth/signin`

**Description** This endpoint signs in a teacher or a student

**Authentication** No

**Request Body**

- `email`
- `password`

**Responses**

Status Code (200)

Created response indicates that the teacher or student has successfully been added

    {
        "token": "string",
        "teacher_id": 1
    }

    or

    {
        "token": "string",
        "student_id": 1
    }

---

Status Code (400)

Bad Request indicates that

- `email` or `password` do not exist in request body
- If `email` and `password` does not match to a teacher

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## signout

**URL** `/auth/signout`

**Description** This endpoint signs out a teacher or a student by setting their token to null

**Authentication** Teacher or Student

**Request Body**

**Responses**

Status Code (200)

Success response indicates that the teacher has been successfully signed out

---

Status Code (401)

Unauthorized indicates that

- `Student-Authorization` or `Teacher-Authorization` header isn't given
- `Student-Authorization` or `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
