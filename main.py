from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends
from auth import verify_token


from auth_service import register_student, login_student
from auth_service import get_user_profile

from evaluation_service import evaluate_submission
from student_service import(
    get_student_by_id,
    create_student
)

from results_service import(
    get_student_results, 
    get_results_by_assessment,
)   
from assessment_service import(
    get_assessments_by_class,
    get_assessment_by_id
)

from question_service import(
    get_questions_by_assessment,
    get_question_by_id
)

from submission_service import(
    create_submission,
    get_submission_by_id
)

from answers_service import(
    submit_answer,
    update_answer,
    get_answers_by_submission
)
class StudentRegister(BaseModel):
    name: str
    email: str
    password: str
    student_class: str
    school: str


class StudentLogin(BaseModel):
    email: str
    password: str


class Student(BaseModel):
    name: str
    student_class: str
    email: str
    school: str

class AnswerRequest(BaseModel):
    question_id: int
    selected_option_id: int = None
    answer_text: str = None

class AnswerUpdate(BaseModel):
    selected_option_id: int = None
    answer_text: str = None

app=FastAPI()


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
    )

def get_current_student(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid token"
            )
    return user


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

@app.get("/assessments")
def get_assessments(
    current_student = Depends(get_current_student)
):

    return get_assessments_by_class(
        current_student["student_class"]
    )

@app.get("/assessments/{assessment_id}")
def get_assessment(assessment_id: int):
    return get_assessment_by_id(assessment_id)

@app.get("/assessments/{assessment_id}/questions")
def get_questions(assessment_id: int):
    return get_questions_by_assessment(assessment_id)

@app.get("/questions/{question_id}")
def get_question(question_id: int):
    return get_question_by_id(question_id)

@app.post("/submissions/{submission_id}/answers")
def submit_answers(
    submission_id: int,
    answers: list[AnswerRequest],
    current_student = Depends(get_current_student)
):
    submission = get_submission_by_id(submission_id)
    if not submission:
        raise HTTPException(
            status_code=404, 
            detail="Submission not found"
            )
    
    if submission[1] != current_student["student_id"]:
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to submit answers for this submission"
            )
    
    for answer in answers:
        submit_answer(
            submission_id,
            answer.question_id,
            answer.selected_option_id
        )
    
    return {"message": "Answers submitted successfully"}

@app.put("/answers/{answer_id}")
def update_answer_api(
    answer_id: int,
    answer: AnswerUpdate,
    current_student = Depends(get_current_student)
):
    return update_answer(
        answer_id,
        answer.selected_option_id,
        answer.answer_text
    )

@app.get("/submissions/{submission_id}/answers")
def get_answers(submission_id: int, current_student = Depends(get_current_student)):
    submission = get_submission_by_id(submission_id)
    if not submission:
        raise HTTPException(
            status_code=404, 
            detail="Submission not found"
            )
    
    if submission[1] != current_student["student_id"]:
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to view answers for this submission"
            )
    
    return get_answers_by_submission(submission_id)


@app.post("/submissions")
def create_submission_api(
    assessment_id: int,
    current_student = Depends(get_current_student)
):
    return create_submission(
        current_student["student_id"],
        assessment_id
    )

@app.get("/submissions/{submission_id}")
def get_submission(submission_id: int, current_student = Depends(get_current_student)):
    submission = get_submission_by_id(submission_id)
    if not submission:
        raise HTTPException(
            status_code=404, 
            detail="Submission not found"
            )
    
    if submission[1] != current_student["student_id"]:
        raise HTTPException(
            status_code=403, 
            detail="You are not authorized to view this submission"
            )
    
    return submission

@app.post("/submissions/{submission_id}/evaluate")
def evaluate_submission_api(
    submission_id: int,
    current_student=Depends(get_current_student)
):
    return evaluate_submission(submission_id)


@app.get("/results")
def get_results(
    current_student = Depends(get_current_student)
):
    return get_student_results(
        current_student["student_id"]
    )

@app.get("/results/assessment/{assessment_id}")
def get_result(
    assessment_id: int,
    current_student = Depends(get_current_student)
):
    return get_results_by_assessment(
        current_student["student_id"],
        assessment_id
    )

@app.post("/register")
def register(student: StudentRegister):
    return register_student(student)



@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    return login_student(
        form_data.username,
        form_data.password
    )


@app.get("/profile")
def get_profile(
    current_student = Depends(get_current_student)
):
    return get_user_profile(
        current_student["student_id"]
    )