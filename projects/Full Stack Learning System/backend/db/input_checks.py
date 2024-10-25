# Functions that are used to check the input into endpoints

# Check if course already exists
def does_course_exist(db, course_code):
    cur = db.cursor()
    qry = """select * from courses where course_code = %s;"""
    cur.execute(qry, [course_code])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False

# Check if thread already exists
def does_thread_exist(db, thread_id):
    cur = db.cursor()
    qry = """select * from threads where thread_id = %s;"""
    cur.execute(qry, [thread_id])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False

# Check if message already exists
def does_message_exist(db, message_id):
    cur = db.cursor()
    qry = """select * from messages where message_id = %s;"""
    cur.execute(qry, [message_id])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False

# Check if question already exists
def does_question_exist(db, question_id):
    cur = db.cursor()
    qry = """select * from questions where question_id = %s;"""
    cur.execute(qry, [question_id])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False

# Check if quiz already exists
def does_quiz_exist(db, quiz_id):
    cur = db.cursor()
    qry = """select * from quizzes where quiz_id = %s;"""
    cur.execute(qry, [quiz_id])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False

# Check if user exists
def does_user_exist(db, user_id):
    cur = db.cursor()
    qry = """select * from users where user_id = %s;"""
    cur.execute(qry, [user_id])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False

# Check if assessments exists
def does_assessment_exist(db, assessment_id):
    cur = db.cursor()
    qry = """select * from assessments where assessment_id = %s;"""
    cur.execute(qry, [assessment_id])
    res = cur.fetchone()
    cur.close()
    if res:
        return True
    return False