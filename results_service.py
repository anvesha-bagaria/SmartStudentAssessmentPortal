from db import conn

def create_result(submission_id, total_marks):
    
    conn.rollback()
    cur= conn.cursor()

    cur.execute(
        """INSERT INTO results (submission_id, total_marks)