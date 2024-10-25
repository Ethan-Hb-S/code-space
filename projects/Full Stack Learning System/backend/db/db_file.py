import db.token_handler
from datetime import datetime, timezone
from db.input_checks import does_course_exist, does_message_exist, does_question_exist

class Db_file():
    def __init__(self, db):
        self.db = db
    
    # Create a file, this file can belong to a question, message or a course
    # Ensure ONLY ONE of course_code, message_id or question_id is NOT None
    def create_file(self, token, name, course_code=None, 
                    message_id=None, question_id=None):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()

        created = datetime.now(timezone.utc)
        if question_id:
            # Check if question exists        
            if not does_question_exist(self.db, question_id):
                return {'Alert' : 'Question does not exist'}
            
            qry = """insert into files(name, created, question)
                    values(%s, %s, %s, %s) 
                    returning file_id;"""
            cur.execute(qry, [name, created, question_id])
        elif message_id:
            # Check if message exists        
            if not does_message_exist(self.db, message_id):
                return {'Alert' : 'Message does not exist'}

            qry = """insert into files(name, created, message)
                    values(%s, %s, %s) 
                    returning file_id;"""
            cur.execute(qry, [name, created, message_id])
        else:
            # Check if course exists        
            if not does_course_exist(self.db, course_code):
                return {'Alert' : 'Course does not exist'}
            
            qry = """insert into files(name, created, course)
                    values(%s, %s, %s) 
                    returning file_id;"""
            cur.execute(qry, [name, created, course_code])

        file_id = cur.fetchone()[0]
        self.db.commit()
        cur.close()
        return {"file_id" : file_id}