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
        "token": "abc",
        "teacher_id": 2
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
