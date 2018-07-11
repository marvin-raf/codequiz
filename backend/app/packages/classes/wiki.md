# Classes Enpoints

[Back to main wiki](#wiki.md)

- ["/classes"](#markdown-header-classes)
- ["/classes/<id>"](#markdown-header-classes-id)
- ["/classes/<id>/students"](#markdown-header-classes-id-students)
- ["/classes/<id>/students/<id>"](#markdown-header-classes-id-students-id)

## `classes`

### GET

**URL** `/classes`

**Description** This endpoint gets all of a teachers classes

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the classes have been successfully retrieved

    {
        "classes": [
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

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

### POST

**URL** `/classes`

**Description** This endpoint creates a class

**Authentication** Teacher

**Request Body**

    {
        "name": "string",
    }

**Responses**
Status Code (201)

Created response indicates the class has been created

    {
        "class_id": 1
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

## `classes id`

### PATCH

**URL** `/classes/<id>`

**Description** This endpoint changes the class name

**Authentication** Teacher

**Request Body**

    {
        "name": "string",
    }

**Responses**
Status Code (200)

Success response indicates the class name has been changed

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

- `class_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `class_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

### DELETE

**URL** `/classes/<id>`

**Description** This endpoint deletes a class

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the class has been deleted

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `class_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates that

- `class_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `classes id students`

### GET

**URL** `/classes/<id>/students`

**Description** This endpoint gets all the students of a class

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the students have been successfully retrieved

    {
        "students": [
            {
                "student_id": 1,
                "student_name": "string",
                "student_email": "string"
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

- `class_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `class_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

### POST

**URL** `/classes/<id>/students`

**Description** This endpoint adds a list of students to the database

**Authentication** Teacher

**Request Body**

    {
        "students: [
            {
                "name": "string",
                "email": "string"
            }
        ]
    }

**Responses**
Status Code (201)

Created response indicates the students have been successfully added

---

Status Code (400)

Bad Request indicates that

- `students` is missing
- `name` is missing in students
- `email` is miisng in students

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `class_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `class_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

### DELETE

**URL** `/classes/<id>/students`

**Description** This endpoint deletes all students in a class

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the students have been successfully deleted

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `class_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `class_id` doesn't match with a class in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---

## `classes id students id`

### DELETE

**URL** `/classes/<id>/students/<id>`

**Description** This endpoint deletes a student from a class

**Authentication** Teacher

**Request Body**

**Responses**
Status Code (200)

Success response indicates the student has been successfully deleted

---

Status Code (401)

Unauthorized indicates that

- `Teacher-Authorization` header isn't given
- `Teacher-Authorization` isn't matched to a teacher in the database

---

Status Code (403)

Forbidden indicates that

- `class_id` and `teacher_id` don't match in the database

---

Status Code (404)

Not Found indicates taht

- `class_id` doesn't match with a class in the database
- `student_id` doesn't match with a student in the database
- `class_id` and `student_id` don't match in the database

---

Status Code (500)

- Server Error indicates anything else that is unexpected and mysql errors

---
