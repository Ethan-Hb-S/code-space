import sys
import psycopg2
import jwt
import config
import db.token_handler

class Db_user:
    def __init__(self, db):
        self.db = db

    # Add a user to the database
    def add_user(self, id, name, email, avatar=None):
        
        # Check if user already exists
        res = self.does_user_exist(id)
        if res['exists'] == True:
            return {'Alert' : 'User already exists'}

        cur = self.db.cursor()

        token = db.token_handler.token_encoder(id)

        if avatar is None:
            qry = """insert into users(user_id, name, email, token)
                    values(%s, %s, %s, %s) returning user_id;"""
            cur.execute(qry, [id, name, email, token])
        else:
            qry = """insert into users(user_id, name, email, token, avatar)
                    values(%s, %s, %s, %s, %s);"""
            cur.execute(qry, [id, name, email, token, avatar])

        self.db.commit()
        cur.close()
        return {'token' : token}

    # Login in a new user
    def user_login(self, id, email):
        cur = self.db.cursor()

        token = db.token_handler.token_encoder(id)

        # Check if user exists
        res = self.does_user_exist(id)
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        qry = """update users set token = %s
                where user_id = %s and email = %s;"""
        cur.execute(qry, [token, id, email])

        self.db.commit()
        cur.close()
        return {'token' : token} 

    # Log out a user
    def user_logout(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if user exists
        res = self.does_user_exist(token_data['user_id'])
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        cur = self.db.cursor()

        qry = """update users set token = null
                where user_id = %s;"""
        cur.execute(qry, [token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}        

    # Set a user to be lecturer/teacher
    def add_lecturer(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if user exists
        res = self.does_user_exist(token_data['user_id'])
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        cur = self.db.cursor()
        
        qry = """insert into lecturers(lecturer_id)
                values(%s);"""
        cur.execute(qry, [token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Set a user to be student
    def add_student(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if user exists
        res = self.does_user_exist(token_data['user_id'])
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        cur = self.db.cursor()
        
        qry = """insert into students(student_id)
                values(%s);"""
        cur.execute(qry, [token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Add a class to the database
    def add_class(self, name, code):
        cur = self.db.cursor()
        
        qry = """insert into classes(name, code) values(%s, %s) 
                returning class_id;"""
        cur.execute(qry, [name, code])

        class_id = cur.fetchone()[0]
        self.db.commit()
        cur.close()
        return {"class_id" : class_id}

    # Enrol students to the database
    def enrol_student(self, student_id, class_id):
        cur = self.db.cursor()

        qry = """insert into Enrolled_in(student, class)
                values(%s, %s)"""
        cur.execute(qry, [student_id, class_id])

        self.db.commit()
        cur.close()

    # Assign user as a teacher
    def assign_teacher(self, lecturer_id, class_id):
        cur = self.db.cursor()

        qry = """insert into Teaches(lecturer, class)
                values(%s, %s)"""
        cur.execute(qry, [lecturer_id, class_id])

        self.db.commit()
        cur.close()
    
    # Check if username is available
    def does_user_exist(self, user_id):
        cur = self.db.cursor()
        qry = """select * from Users where user_id = %s"""
        cur.execute(qry, [user_id])
        names = cur.fetchall()
        if not names:
            return {"exists" : False}

        cur.close()
        return {"exists" : True}

    # Get details about a particular user
    def get_user_info(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if user exists
        res = self.does_user_exist(token_data['user_id'])
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        cur = self.db.cursor()
        
        qry = """select * from Users where user_id = %s"""
        cur.execute(qry, [token_data['user_id']])
        user = cur.fetchone()
        cur.close()
        if user == None:
            return None

        return user

    # Check if the current user is a lecturer
    def is_lecturer(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if user exists
        res = self.does_user_exist(token_data['user_id'])
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        cur = self.db.cursor()
        
        qry = """select * from lecturers where lecturer_id = %s"""
        cur.execute(qry, [token_data['user_id']])
        names = cur.fetchall()
        if not names:
            cur.close()
            return {'is_lecturer' : False}
        
        cur.close()
        return {'is_lecturer' : True}

    # Update the avatar of the current user
    def update_avatar(self, token, avatar):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if user exists
        res = self.does_user_exist(token_data['user_id'])
        if not res['exists']:
            return {'Alert' : 'User does not exist'}

        cur = self.db.cursor()

        qry = """update users set avatar = %s where user_id = %s"""
        cur.execute(qry, [avatar, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}
