# SmartStudentAssessmentPortal
student assessment portal built with FastAPI that allows students to register,
log in, attempt assessments, submit answers, and view their results.
Supports both objective (MCQ) and subjective question types with 
automated evaluation.

## Features

- Student registration and login with JWT authentication
- View assessments filtered by student class
- Create submissions and submit objective + subjective answers
- Automated evaluation of MCQ answers
- AI based evaluation for subjective answers
- View results and feedback per assessment

## Tech Stack

Backend: FastAPI
Database: PostgreSQL
Authentication: JWT (JSON Web Tokens)
Password Hashing: bcrypt via passlib
ORM: Raw SQL via psycopg2

## Authentication

This API uses JWT Bearer tokens. To access protected endpoints:

1. Register via `POST /register`
2. Login via `POST /login` to get your token
3. In Swagger UI, click on authorize button and enter username and password
4. All protected routes will now work

## Error Codes

| 200 | Success |
| 201 | Created successfully |
| 400 | Bad request / invalid input |
| 401 | Unauthorized / invalid token / wrong password |
| 403 | Forbidden / accessing another student's data |
| 404 | Resource not found |
| 409 | Conflict / email already registered |
| 500 | Internal server error |