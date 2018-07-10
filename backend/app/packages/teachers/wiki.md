# Teachers Endpoints

- ["/teachers/signup"](#signup)
- ["/teachers/signin"](#signin)
- ["/teachers/signout"](@signout)

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
