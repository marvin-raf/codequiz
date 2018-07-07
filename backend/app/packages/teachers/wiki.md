# Teachers Endpoints

- ["/teachers/signup"](#signup)
- ["/teachers/signin"](#signin)

## signup

**URL** `/teachers/signup`

**Description** This endpoint signs up a teacher

**Authentication** No

**Request Body**

- `name`
- `email`
- `password`

**Responses**

Status Code (201)

Created response indicates that the teacher has been successfully signed up

    {
        "teacher_id": 1
    }

---

Status Code (400)

Bad Request indicates that

- `name` or `email` or `password` do not exist in request body
- If `email` is already taken

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## signin

**URL** `/teachers/signin`

**Description** This endpoint signs in a teacher

**Authentication** No

**Request Body**

- `email`
- `password`

**Responses**

Status Code (200)

Created response indicates that the teacher has successfully signed in

    {
        "token": "string",
        "teacher_id": 1
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

**URL** `/teachers/signout`

**Description** This endpoint signs out a teacher by setting their token to null

**Authentication** Teacher

**Request Body**

**Responses**

Status Code (200)

Success response indicates that the teacher has been successfully signed out

---

Status Code (401)

Unauthorized indicates that

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
