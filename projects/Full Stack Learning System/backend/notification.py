import smtplib
import ssl
import config
import db.token_handler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from db.input_checks import does_course_exist, does_thread_exist,  does_assessment_exist

class Db_notification():
    def __init__(self, db):
        self.db = db

    def notify(self, student_name, email, task_id, course_name, flag):
        # Default SMTP config
        smtp_port = 465
        smtp_server = "mail.iweb.com.br"
        EMAIL = config.EMAIL
        EMAIL_PASSWORD = config.EMAIL_PASSWORD

        # Notify on new thread
        if (flag == "forum"):
            subject = f"New thread in {course_name}"
            body = f"Hi {student_name}!,\n There is a new thread titled \"{task_id}\" in {course_name}."
        else:
            subject = f"New course material has been uploaded for {course_name}"
            body = f"Hi {student_name}!,\n Your teacher has posted a new material titled \"{task_id}\" in {course_name}."

        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(EMAIL, EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()

    # Notify students of a new thread in a class
    def notify_forum(self, token, thread_id, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if thread exists
        if not does_thread_exist(self.db, thread_id):
            return {'Alert' : 'Thread does not exist'}

        # Check if course exists
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        # Get list of students in this course
        course = self.get_student_in_class_info(course_code)

        # For each of the students notify!
        for student in course:
            self.notify(student[0], student[1], self.thread_name(thread_id)[0] ,student[2], "forum")
        return {}

    def notify_course_material(self, token, material_name, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if course exists
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        # Get list of students in this course
        course = self.get_student_in_class_info(course_code)

        # For each of the students notify!
        for student in course:
            self.notify(student[0], student[1], material_name, student[2], "course_material")
        return {}

    def get_student_in_class_info(self, course_code):
        cur = self.db.cursor()
        qry = '''select u.name, u.email, c.name as course_name from users u
                    join enrolled_in e on e.student = u.user_id
                    join courses c on c.course_code = e.course
                    where e.course = %s;
                '''
        cur.execute(qry, [course_code])
        students = cur.fetchall()
        cur.close()
        return students

    def thread_name(self, thread_id):
        cur = self.db.cursor()
        qry = '''select thread_title from threads where thread_id = %s;
                '''
        cur.execute(qry, [thread_id])
        thread = cur.fetchone()
        cur.close()
        return thread
