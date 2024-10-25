import requests
import config
import json
import time
import db.token_handler
from db.input_checks import does_course_exist

class Db_course():
    def __init__(self, db):
        self.db = db
        self.access_token = None
        self.access_token_created = None

    # Get all users in a course
    def add_course(self, token, name, code, description):

        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if course already exists        
        if does_course_exist(self.db, code):
            return {'Alert' : 'Course already exists'}

        cur = self.db.cursor()
        qry = """insert into courses(course_code, name, description) 
                 values(%s, %s, %s);"""
        cur.execute(qry, [code, name, description])

        qry = """insert into teaches(lecturer, course) values(%s, %s);"""
        cur.execute(qry, [token_data['user_id'], code])

        self.db.commit()
        cur.close()
        return {}

    # Get all information about a particular course
    def course_data(self, token, course_code):

        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if course exists        
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        cur = self.db.cursor()
        # Get all information about a course
        qry = """select * from courses where course_code = %s;"""
        cur.execute(qry, [course_code])
        res = cur.fetchone()

        code, name, description = res[0], res[1], res[2]

        # Get all students and lecturers in a course
        lecturers = []
        qry = """
            select u.user_id, u.name
            from users u 
                join lecturers l on l.lecturer_id = u.user_id 
                join teaches t on t.lecturer = l.lecturer_id 
            where t.course = %s
        """
        cur.execute(qry, [course_code])
        for each in cur.fetchall():
            lecturers.append({'user_id': str(each[0])[-8:], 'user_name':each[1]})
        
        students = []
        qry = """
            select u.user_id, u.name
            from users u 
                join students s on s.student_id = u.user_id 
                join enrolled_in e on e.student = s.student_id 
            where e.course = %s
        """
        cur.execute(qry, [course_code])
        for each in cur.fetchall():
            students.append({'user_id': str(each[0])[-8:], 'user_name':each[1]})

        # Get all assessments in a course
        assessments = []
        qry = """
            select * from assessments a 
            where course = %s
        """
        cur.execute(qry, [course_code])
        for each in cur.fetchall():
            assessments.append({"name" : each[1], "due_date" : each[3]})

        cur.close()

        return {
            'name' : name,
            'code' : code,
            'description' : description,
            'assessments' : assessments,
            'lecturers' : lecturers,
            'students' : students
        }
    
    # Allow user to join course
    def join_course(self, token, course_code):

        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        # Check if course exists
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}
        
        cur = self.db.cursor()
        qry = """insert into enrolled_in(student, course) values(%s, %s);"""
        cur.execute(qry, [token_data['user_id'], course_code])

        self.db.commit()    
        cur.close()
        return {}

    # Get all courses that a particular user is enrolled in or teaches
    def list_courses(self, token):
        token_data = db.token_handler.token_decoder(token)
        
        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Courses which the user is enrolled in
        cur = self.db.cursor()
        enrolled = []
        qry = """select * from courses c
                    join enrolled_in e on c.course_code=e.course
                    where e.student=%s;"""
        cur.execute(qry, [token_data['user_id']])
        for each in cur.fetchall():
            enrolled.append({'code':each[0], 'name':each[1], 'description':each[2]})
        
        # Courses which the user teaches
        teaches = []
        qry = """select * from courses c
                 join teaches t on c.course_code=t.course 
                 where t.lecturer=%s;"""
        cur.execute(qry, [token_data['user_id']])
        for each in cur.fetchall():
            teaches.append({'code':each[0], 'name':each[1], 'description':each[2]})
        cur.close()

        return {
            'student_of' : enrolled,
            'teaches' : teaches
        }

    # After a zoom link is generated, store it in the database
    def zoom_details_db(self, course_code, zoom_url, zoom_status, 
                        zoom_start_time, zoom_password):
        cur = self.db.cursor()

        qry = """insert into Zoom_meetings(zoom_url, status, start_time, zoom_password) 
                 values(%s, %s, %s, %s) returning zoom_id"""
        cur.execute(qry, [zoom_url, zoom_status, zoom_start_time, zoom_password])
        zoom_id = cur.fetchone()[0]
        self.db.commit() 

        qry = """insert into Zoom_per_class(course, zoom_id) values(%s, %s)"""
        cur.execute(qry, [course_code, zoom_id])
        self.db.commit()
        cur.close()

        return zoom_id

    # Get a zoom access token
    def get_zoom_access_token(self):
        payload = {"grant_type" : "account_credentials", 
                   "account_id" : config.ZOOM_ACCOUNT_ID}
        res = requests.post("https://zoom.us/oauth/token", data=payload,
                            auth=(config.ZOOM_CLIENT_ID, config.ZOOM_CLIENT_SECRET))
        if res.status_code == 200 or res.status_code == 201:
            self.access_token_created = time.time()
            return res.json()['access_token']
        else:
            return None

    # Generate the zoom link using the Zoom API
    def generate_zoom_link(self, token, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        # Check if course exists        
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        # Access token has not been created yet so create one
        if self.access_token_created == None:
            self.access_token = self.get_zoom_access_token()
        
        # If the access token has expired create another one
        if time.time() - self.access_token_created > 3300:
            self.access_token = self.get_zoom_access_token()
        
        payload = {
            "topic": f"{course_code} Meeting",
            "type":"2",
            "start_time": "2022-07-17T22:10:10Z",
            "duration":"2",
            "settings":{
                "host_video":"true",
                "participant_video":"true",
                "join_before_host":"true",
                "mute_upon_entry":"true",
                "watermark": "true",
                "audio": "voip",
                "auto_recording": "cloud"
            }     
        }
        payload = json.dumps(payload)
        the_headers = {
            'Authorization' : "Bearer " + self.access_token,
            'Content-Type' : "application/json"
        }
        res = requests.post("https://api.zoom.us/v2/users/me/meetings", 
                            data=payload, headers=the_headers)
        join_url, status, start_time, password = None, None, None, None

        # If we get a response
        if res.status_code == 200 or res.status_code == 201:
            join_url = res.json()['join_url']
            status = res.json()['status']
            start_time = res.json()['start_time']
            password = res.json()['password']
            zoom_id = self.zoom_details_db(course_code, join_url, 
                                           status, start_time, password)
            return {'zoom_id' : zoom_id, 'zoom_url' : join_url, 
                    'status' : status, 'start_time' : start_time, 
                    'password' : password}
        
        return {'Alert' : 'Zoom link could not be automatically generated'}
    
    # Get a zoom link that already exists and is not expired
    def get_zoom_link(self, token, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if course exists        
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        cur = self.db.cursor()
        qry = """select * from Zoom_meetings z
                    join Zoom_per_class p on z.zoom_id = p.zoom_id 
                    where p.course = %s;"""
        cur.execute(qry, [course_code])
        zoom_details = cur.fetchone()
        cur.close()

        if not zoom_details:
            return {'Alert' : 'No previous zoom links created'}

        return {'zoom_id' : zoom_details[0], 'zoom_url' : zoom_details[1], 
                'status' : zoom_details[2], 'start_time' : zoom_details[3], 
                'password' : zoom_details[4]}
    
    # Get files that teacher has uploaded
    def get_course_files(self, token, course_code):
        token_data = db.token_handler.token_decoder(token)
        
        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()
        qry = """select file_id, name from files where course = %s"""
        cur.execute(qry, [course_code])
        details = cur.fetchall()
        names = []
        for file in details:
            names.append(file[1])
        cur.close()
        return names
    
    # Used to search class material
    def search_material(self, token, course_code, search_word):
        token_data = db.token_handler.token_decoder(token)
        
        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        cur = self.db.cursor()
        
        # Get all assessments that contain search word
        assessments = []
        qry = """select assessment_id, due_date, title 
                    from assessments 
                    where course = %s and 
                    title ILIKE '%%' || %s ||'%%';"""
        cur.execute(qry, [course_code, search_word])
        results = cur.fetchall()
        for res in results:
            assessments.append({'assessment_id' : res[0], 
                                'due_date' : res[1], 
                                'title' : res[2]})
        
        # Get all files that contain search word
        files = []
        qry = """select name 
                    from files 
                    where course = %s and name ILIKE '%%' || %s ||'%%';"""
        cur.execute(qry, [course_code, search_word])
        results = cur.fetchall()
        for res in results:
            files.append(res[0])
        cur.close()
        return {'assessments' : assessments, 'files' : files}
