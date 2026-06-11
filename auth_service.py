from db import conn
from pydantic import BaseModel
from passlib.context import CryptContext
from auth import create_access_token


class StudentRegister(BaseModel):
    student_id: int 
    name: str
    email:str
    password:str
    student_class:str
    school:str


def register_student(student):
    cur=conn.cursor()

    cur.execute(
        """SELECT student_id
        FROM students
        WHERE email= %s
        """,
        (student.email,)
    )
    
    existing_student = cur.fetchone()

    if existing_student:
        cur.close()
        return {"message": "Email already registered"}
    
    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto"
    )
    
    hashed_password = pwd_context.hash(student.password)
    
    cur.execute(
        """INSERT INTO students (name, email, password,student_class,school)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING student_id
        """,
        (student.name, student.email, hashed_password, student.student_class, student.school)
    )
    conn.commit()

    cur.close()
    conn.close()

    return {"message": "Student registered successfully"}

def login_student(email, password):
    cur = conn.cursor()

    cur.execute(
        """
        SELECT student_id, name, email, password
        FROM students
        WHERE email = %s
        """,
        (email,)
    )

    student = cur.fetchone()

    if not student:
        cur.close()
        return {"message": "Student not found"}

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    if not pwd_context.verify(password, student[3]):
        cur.close()
        return {"message": "Invalid password"}

    access_token = create_access_token({"student_id": student[0], "email": student[2]})

    cur.close()
    # do not close global conn here; let caller manage connection lifecycle if needed

    return {"access_token": access_token, "token_type": "bearer"}     

def get_user_profile(student_id):

    cur = conn.cursor()

    cur.execute(
        """
        SELECT student_id, name, email, student_class, school
        FROM students
        WHERE student_id = %s
        """,
        (student_id,)
    )

    return cur.fetchone()

