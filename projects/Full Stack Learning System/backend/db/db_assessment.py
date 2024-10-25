# All functions related to assessments

from datetime import datetime, timezone
from db.input_checks import does_course_exist
import db.token_handler

class Db_assessment():
    def __init__(self, db):
        self.db = db
    
    # Create a new assessment
    def create_assessment(self, token, title, description, due_date,
                          marks, hidden, course_code, file_name=None):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if course exists        
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        cur = self.db.cursor()

        created = datetime.now(timezone.utc)

        qry = """insert into 
                assessments(title, description, due_date, marks, hidden, course)
                values(%s, %s, %s, %s, %s, %s) 
                returning assessment_id;"""
        cur.execute(qry, [title, description, due_date, marks, 
                          hidden, course_code])

        assessment_id = cur.fetchone()[0]
        self.db.commit()

        # If a file was uploaded, then create a file
        if file_name:
            qry = """insert into files(name, created, assessment)
                    values(%s, %s, %s) 
                    returning file_id;"""
            cur.execute(qry, [file_name, datetime.now(), assessment_id])            
            self.db.commit()
        file_id = cur.fetchone()[0]
        cur.close()
        return {"assessment_id" : assessment_id, "file_id" : file_id}  

    # Update an existing assessment
    def update_assessment(self, token, hidden, assessment_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        cur = self.db.cursor()

        created = datetime.now(timezone.utc)

        qry = """update assessments set hidden = %s
                where assessment_id = %s;"""
        cur.execute(qry, [hidden, assessment_id])

        self.db.commit()
        cur.close()
        return {}     
    
    # Get all assessments (that are still due) of a particular user
    def get_open_assessments(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        cur = self.db.cursor()
        qry = '''select a.title, a.due_date, a.course
                from assessments a
                join (
                    select MIN(due_date) as earliest_date, course
                    from assessments
                    where due_date > NOW()
                    group by course
                ) as res on a.course = res.course
                and a.due_date = res.earliest_date
                join enrolled_in e on e.course = a.course
                where e.student = %s;'''
        cur.execute(qry, [token_data['user_id']])

        assts = []
        for asst in cur.fetchall():
            assts.append({'asstName': asst[0] ,'due_date' : asst[1], 'course' : asst[2]})
        cur.close()

        return assts

    # Get all open assessments for a particular course
    def get_assessments_course(self, course):

        cur = self.db.cursor()
        qry = '''select assessment_id, title, due_date from assessments
                where course = %s
                and due_date > NOW()'''
        cur.execute(qry, [course])

        assts = []
        for asst in cur.fetchall():
            assts.append({'id': asst[0], 'title': asst[1], 'due_date': asst[2]})
        
        cur.close()
        return assts

    # Get assessment results of a particular user in a course (STUDENT)
    def get_assessment_results(self, token, course):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        cur = self.db.cursor()
        qry = '''select a.assessment_id, a.title, t.mark as received_mark, 
                 a.marks as total_marks, a.course
                 from assessments a
                 join asst_submissions t on t.assessment_id = a.assessment_id
                 where a.due_date < NOW()
                 and t.student_id = %s
                 and a.course = %s;'''

        cur.execute(qry, [token_data['user_id'], course])

        assts = []
        for asst in cur.fetchall():
            assts.append({'id':asst[0], 'asstName': asst[1], 'mark': f'{asst[2]} / {asst[3]}'})
        cur.close()
        return assts

    def get_student_results(self, token, studentId, course):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        cur = self.db.cursor()
        qry = '''select a.assessment_id, a.title, t.mark as received_mark, 
                 a.marks as total_marks, a.course
                 from assessments a
                 join asst_submissions t on t.assessment_id = a.assessment_id
                 where t.student_id = %s
                 and a.course = %s;'''

        cur.execute(qry, [studentId, course])

        assts = []
        for asst in cur.fetchall():
            assts.append({'id':asst[0], 'asstName': asst[1], 'mark': asst[2], 'outOf': f' / {asst[3]}', 'quiz': False})
        cur.close()
        return assts

    # Let user submit an assignment
    def submit_assessment(self, token, assessment, file_name=None):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()

        submission_date = datetime.now(timezone.utc)
        qry = """insert into asst_submissions(submission_date, 
                student_id, assessment_id)
                values(%s, %s, %s) 
                returning submission_id;"""
        cur.execute(qry, [submission_date, token_data['user_id'], 
                          assessment])

        submission_id = cur.fetchone()[0]
        self.db.commit()

        # If a file was uploaded, then create a file
        if file_name:
            qry = """insert into files(name, created, asst_submission)
                    values(%s, %s, %s) 
                    returning file_id;"""
            cur.execute(qry, [file_name, datetime.now(), submission_id])           
            self.db.commit()
        file_id = cur.fetchone()[0]
        cur.close()
        return {"submission_id" : submission_id, "file_id" : file_id}  
   
    # Let user edit an assignment submission
    def mark_submission(self, token, mark, assessment, student_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()

        qry = """update asst_submissions
                set mark = %s
                where assessment_id = %s and student_id = %s;"""
        cur.execute(qry, [mark, assessment, student_id])

        self.db.commit()
        cur.close()
        return {} 

    # Get assessment file
    def get_assessment_file(self, token, assessment_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()

        qry = """select name from files where assessment = %s;"""
        cur.execute(qry, [assessment_id])

        files = []
        for file in cur.fetchall():
            files.append(file[0])

        cur.close()
        return {'files' : files} 

    # Get a students submitted file
    def get_submission_file(self, token, assessment_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()

        qry = """select f.name as file_name, u.name as student_name from files f
                    join asst_submissions s on s.submission_id = f.asst_submission
                    join users u on u.user_id = s.student_id 
                    where s.assessment_id = %s;"""
        cur.execute(qry, [assessment_id])

        files = []
        for file in cur.fetchall():
            files.append({'student': file[1], 'file': file[0]})

        cur.close()
        return {'files' : files}   