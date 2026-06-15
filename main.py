from fastapi import FastAPI

from fastapi.security import OAuth2PasswordBearer

from router import auth_router, assessments, submissions, answers, results

from schemas import Student

from student_service import(
    get_student_by_id,
    create_student
)

app=FastAPI()


app.include_router(auth_router.router)
app.include_router(assessments.router)
app.include_router(submissions.router)
app.include_router(answers.router)
app.include_router(results.router)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
    )


@app.get("/students/{student_id}")
def student(student_id: int):
    return get_student_by_id(student_id)

@app.post("/students")
def add_student(student: Student):
    return create_student(
        student.name,
        student.student_class, 
        student.email, 
        student.school
        )
