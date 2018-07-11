# Students Endpoints

[Back to main wiki](../../../wiki.md)

- ["/students/activate"](#students-activate)
- ["/students/parse"](#students-parse)

## `students activate`

### POST

**URL** `/students/activate`

**Description** This endpoint activates a student by setting their password

**Authentication** No

**Request Body**

    {
        "activate_token": "string",
        "password": "string"
    }

**Responses**
Status Code (201)

Success response indicates the student has been activated and have set their password

---

Status Code (400)

Bad Request indicates that

- `activate_token` or `password` do not exist in request body
- `activate_token` does not exist in student table

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `students parse`

### POST

**URL** `/students/parse`

**Description** This endpoint parses an excel document into a list of students

**Authentication** Teacher

**Request Body** - NOTE: Request body should be FormData NOT JSON

    FormData = {"excel_doc": excel_doc}

**Responses**
Status Code (200)

Success response indicates that the excel document has been parsed successfully.

---

Status Code (400)

Bad Request indicates that

- `excel_doc` image was not uploaded
- `excel_doc` was not an excel document
- The headers (email, name) or (email, first_name, last_name) of `excel_doc` were incorrect

---

Status Code (401)

Unauthorized indicates that

- `X-Authorization` header isn't given
- `X-Authorization` isn't matched to a teacher in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
