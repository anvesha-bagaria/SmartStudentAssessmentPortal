from db import conn

def submit_answer(
    submission_id,
    question_id,
    selected_option_id
):
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO submitted_answers
        (
            submission_id,
            question_id,
            selected_option_id
        )
        VALUES (%s, %s, %s)
        """,
        (
            submission_id,
            question_id,
            selected_option_id
        )
    )

    conn.commit()

    return {
        "message": "Answer submitted successfully"
    }


def update_answer(answer_id, selected_option_id):
    conn.rollback()
    cur=conn.cursor()

    cur.execute(
        """UPDATE submitted_answers
        SET selected_option = %s
        WHERE answer_id = %s
        """,
        (selected_option_id, answer_id)
    )

    conn.commit()

    return {"message": "Answer updated successfully"}

def get_answers_by_submission(submission_id):
    conn.rollback()
    cur=conn.cursor()

    cur.execute(
        """SELECT answer_id, question_id, selected_option
        FROM submitted_answers
        WHERE submission_id = %s
        """,
        (submission_id,)
    )

    return cur.fetchall()