from db import conn

def get_questions_by_assessment(assessment_id):
    conn.rollback()
    cur=conn.cursor()

    cur.execute(
        """SELECT question_id, question_text, options, correct_answer
        FROM questions
        WHERE assessment_id = %s
        """,
        (assessment_id,)
    )

    return cur.fetchall()

def get_question_by_id(question_id):
    conn.rollback()
    cur=conn.cursor()

    cur.execute(
        """SELECT question_id, question_text, options, correct_answer
        FROM questions
        WHERE question_id = %s
        """,
        (question_id,)
    )

    return cur.fetchone()
