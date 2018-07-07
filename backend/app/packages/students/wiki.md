# Students Endpoints

- ["/students/activate"](#activate)
- ["/signin"](#signin)

## activate

**URL** `/students/activate`

**Description** This endpoint activates a student by setting their password

**Authentication** No

**Request Body**

- `activate_token`
- `password`

**Responses**
Status Code (200)

Success response indicates the student has been activated and have set their password

---

Status Code (400)

Bad Request indicates that

- `activate_token` or `password` do not exist in request body
- `activate_token` does not exist in student table

---

Status Code (500)

Server Error indicates anything else that is unexpected and mysql errors

---

## signin

**URL** `/students/signin`

**Description** This endpoint signs in a student and returns their token and student_id

**Authentication** No

**Request Body**

- `email`
- `password`

**Responses**
Status Code (200)

Success response indicates the student has been signed in

    {
        "token": "123",
        "student_id": 1
    }

---

Status Code (400)

Bad Request indicates that

- `email` or `password` do not exist in request body
- `email` and `password` do not match to a user

---

Status Code (500)

Server Error indicates anything else that is unexpected and mysql errors

---
