from db import conn

def get_all_assessments():
    conn.rollback()
    cur=conn.cursor()

    cur.execute(
        "SELECT * FROM assessments"
    )

    return cur.fetchall()

def get_assessment_by_id(assessment_id):
    conn.rollback()
    cur=conn.cursor()

    cur.execute(
        """SELECT * FROM assessments
        WHERE assessment_id = %s
        """,
        (assessment_id,)            
    )
    return cur.fetchone()
