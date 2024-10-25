import datetime
import io
from flask import Flask, render_template, url_for, request, redirect, session, send_file
from authlib.integrations.flask_client import OAuth
from authlib.common.security import generate_token
from flask_cors import CORS
import config
import os
from google.cloud import storage
from chatbot import *

# Database imports
import psycopg2
from db.db_user import Db_user
from db.db_course import Db_course
from db.db_forum import Db_forum
from db.db_file import Db_file
from db.db_assessment import Db_assessment
from db.db_quiz import Db_quiz
from db.create_table_queries import queries
from db.db import init_db_command
from notification import Db_notification
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './serviceAccKey.json'

# Connect to database
db = psycopg2.connect(host=config.HOST, port=config.PORT,
                      database=config.DATABASE, user=config.USER,
                      password=config.PASSWORD)

# Create database tables if it not created already
try:
    init_db_command(db)
except Exception as err:
    pass

# Setup access to database
user_db = Db_user(db)
course_db = Db_course(db)
forum_db = Db_forum(db)
file_db = Db_file(db)
assessment_db = Db_assessment(db)
quiz_db = Db_quiz(db)
notification = Db_notification(db)

# Flask setup
app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['TRAP_HTTP_EXCEPTIONS'] = True
CORS(app)
oauth = OAuth(app)
storage_client = storage.Client(project='yellowfrogs')

@app.route('/')
def home():
    return 'Hi'

#==============================================================================
# Courses
#==============================================================================

# Create a course
@app.route('/create/course', methods=['POST'])
def courses_create():
    info = request.get_json()
    return course_db.add_course(info['token'], info['name'],
                                info['code'], info['description'])

# List all data about a course
@app.route('/course/list', methods=['GET'])
def course_list():
    token = request.args.get('token')
    course_code = request.args.get('course_code')
    return course_db.course_data(token, course_code)

# User can join a course
@app.route('/course/join', methods=['POST'])
def course_join():
    info = request.get_json()
    return course_db.join_course(info['token'], info['course_code'])

# List courses that user teaches or is student of
@app.route('/user/courses', methods=['GET'])
def user_courses():
    token = request.args.get('token')
    return course_db.list_courses(token)

# Generate a zoom link for a class
@app.route('/generate/zoom', methods=['POST'])
def generate_zoom():
    info = request.get_json()
    return course_db.generate_zoom_link(info['token'], info['course_code'])

# Send existing zoom url
@app.route('/get/zoom', methods=['GET'])
def get_zoom_link():
    token = request.args.get('token')
    course_code = request.args.get('course_code')
    return course_db.get_zoom_link(token, course_code)

# Search class material (assessments, quizzes)

@app.route('/search/material', methods=['GET'])
def search_material():
    token = request.args.get('token')
    course_code = request.args.get('course_code')
    search_word = request.args.get('search_word')
    return course_db.search_material(token, course_code, search_word)

#==============================================================================
# Assessments
#==============================================================================

# Create an assessment, this will be hidden from students
@app.route('/create/assessment', methods=['POST'])
def assessment_create():
    info = request.get_json()
    file_name = info['file_name'] if 'file_name' in info else None
    return assessment_db.create_assessment(info['token'], info['title'],
                                           info['description'],
                                           info['due_date'],
                                           info['marks'], info['hidden'],
                                           info['course_code'],
                                           file_name)

# Publish an assessment, this will be visible to students
@app.route('/publish/assessment', methods=['POST'])
def assessment_publish():
    info = request.get_json()
    return assessment_db.update_assessment(info['token'], info['hidden'],
                                           info['assessment_id'])

# Get list of open assessments for a specific user
@app.route('/open/assessments', methods=['GET'])
def open_assessments():
    token = request.args.get('token')
    return assessment_db.get_open_assessments(token)

# Get list of open assessments for a course
@app.route('/course/assessments', methods=['GET'])
def course_assessments():
    course = request.args.get('course')
    return assessment_db.get_assessments_course(course)

# Get list of closed assessments and results for a user in a course (STUDENT)
@app.route('/assessments/results', methods=['GET'])
def assessment_results():
    token = request.args.get('token')
    course = request.args.get('course')
    return assessment_db.get_assessment_results(token, course)

# Get list of results for a user as a teacher in a course (TEACHER)
@app.route('/student/results', methods=['GET'])
def student_results():
    token = request.args.get('token')
    studentId = request.args.get('studentId')
    course = request.args.get('course')
    return assessment_db.get_student_results(token, studentId, course)

# Submit an assignment for user
@app.route('/submit/assessment', methods=['POST'])
def submit_a_assessment():
    info = request.get_json()
    file_name = info['file_name'] if 'file_name' in info else None
    return assessment_db.submit_assessment(info['token'],
                                           info['assessment'],
                                           file_name)

# Mark an assignment
@app.route('/mark/assessment', methods=['POST'])
def mark_a_submission():
    info = request.get_json()
    return assessment_db.mark_submission(info['token'], info['mark'],
                                         info['assessment'],
                                         info['student_id'])

# Get list of all assessment files
@app.route('/assessment/files', methods=['GET'])
def assessment_files():
    token = request.args.get('token')
    assessment_id = request.args.get('assesssment_id')
    return assessment_db.get_assessment_file(token, assessment_id)

# Get list of a students submitted file for an assessment
@app.route('/submitted/files', methods=['GET'])
def submitted_files():
    token = request.args.get('token')
    assessment_id = request.args.get('assessment_id')
    return assessment_db.get_submission_file(token, assessment_id)


#==============================================================================
# Files
#==============================================================================

# Upload a file
# The file can belong to ONE of the following: course, message,
# thread or question
@app.route('/upload/file', methods=['POST'])
def file_create():
    info = request.get_json()
    course_code = info['course_code'] if 'course_code' in info else None
    message_id = info['message_id'] if 'message_id' in info else None
    question_id = info['question_id'] if 'question_id' in info else None
    return file_db.create_file(info['token'], info['name'],
                               course_code, message_id, question_id)

# Upload to GCS
@app.route('/upload/cloud', methods=['POST'])
def upload_cloud():
    files = request.files
    for key, file in files.items():
        bucket = storage_client.bucket('3900yellowfrogs_storage')
        blob = bucket.blob(key)
        blob.upload_from_file(file)
    return ""

# Retrieve file from GCS
@app.route('/retrieve/files/cloud', methods=['GET'])
def retrieve_cloud():
    filename = request.args.get('fileName', None)
    bucket = storage_client.bucket('3900yellowfrogs_storage')
    res = {}
    if filename:
        blob = bucket.get_blob(filename)
        res[blob.name] = blob.generate_signed_url(
                            expiration=datetime.timedelta(minutes=10),
                        )
    else:
        blobs = bucket.list_blobs()
        for b in blobs:
            res[b.name] = b.generate_signed_url(
                            expiration=datetime.timedelta(minutes=10),
                        )
    return res

# # Get course materials
@app.route('/files/list', methods=['GET'])
def get_files():
    token = request.args.get('token')
    code = request.args.get('code')
    return course_db.get_course_files(token, code)

#==============================================================================
# Users
#==============================================================================

# Check if user is teacher
@app.route('/user/is_lecturer', methods=['GET'])
def is_lecturer():
    token = request.args.get('token')
    return user_db.is_lecturer(token)

# Check if user exists
@app.route('/user/exists', methods=['GET'])
def user_exists():
    user_id = request.args.get('user_id')
    return user_db.does_user_exist(user_id)

# Add a new user (i.e. register)
@app.route('/user/add', methods=['POST'])
def user_add():
    info = request.get_json()
    return user_db.add_user(info['user_id'], info['name'],
                            info['email'], None)

# User can log-in
@app.route('/user/login', methods=['POST'])
def user_login():
    info = request.get_json()
    return user_db.user_login(info['user_id'], info['email'])

# User can logout
@app.route('/user/logout', methods=['POST'])
def user_logout():
    info = request.get_json()
    return user_db.user_logout(info['token'])

# Add a new lecturer
@app.route('/user/add_lecturer', methods=['POST'])
def add_lecturer():
    info = request.get_json()
    return user_db.add_lecturer(info['token'])

# Add a new student
@app.route('/user/add_student', methods=['POST'])
def add_student():
    info = request.get_json()
    return user_db.add_student(info['token'])

# Update a user's avatar
@app.route('/user/avatar', methods=['PUT'])
def user_update_avatar():
    info = request.get_json()
    return user_db.update_avatar(info['token'], info['avatar'])

# Get user info
@app.route('/user', methods=['GET'])
def user_info():
    token = request.args.get('token')
    user_info = user_db.get_user_info(token)
    return { 'name': user_info[1], 'email': user_info[2],
            'avatar': user_info[4] }

#==============================================================================
# Forums
#==============================================================================

# Add a new thread
@app.route('/thread/add', methods=['POST'])
def add_thread():
    info = request.get_json()
    return forum_db.add_thread(info['token'], info['title'], info['course'])

# Pin the thread
@app.route('/thread/pin', methods=['POST'])
def pin_thread():
    info = request.get_json()
    return forum_db.pin_thread(info['token'], info['thread_id'])

# Unpin the thread
@app.route('/thread/unpin', methods=['DELETE'])
def unpin_thread():
    info = request.get_json()
    return forum_db.unpin_thread(info['token'], info['thread_id'])

# List all threads in a course
@app.route('/threads/list', methods=['GET'])
def list_threads():
    token = request.args.get('token')
    course = request.args.get('course_code')
    return forum_db.list_threads(token, course)

# Add a new message
@app.route('/message/add', methods=['POST'])
def add_message():
    info = request.get_json()
    file_name = info['file_name'] if 'file_name' in info else None
    return forum_db.add_message(info['token'], info['message'],
                                info['thread'], file_name)

# List all messages in a thread
@app.route('/message/list', methods=['GET'])
def list_messages():
    token = request.args.get('token')
    thread_id = request.args.get('thread_id')
    return forum_db.list_messages(token, thread_id)

# Pin the message
@app.route('/message/pin', methods=['POST'])
def pin_message():
    info = request.get_json()
    return forum_db.pin_message(info['token'], info['message_id'])

# Unpin the message
@app.route('/message/unpin', methods=['POST'])
def unpin_message():
    info = request.get_json()
    return forum_db.unpin_message(info['token'], info['message_id'])

# Like the message
@app.route('/message/like', methods=['POST'])
def like_message():
    info = request.get_json()
    return forum_db.like_message(info['token'], info['message'])

# Unlike the message
@app.route('/message/unlike', methods=['DELETE'])
def unlike_message():
    info = request.get_json()
    return forum_db.unlike_message(info['token'], info['message'])

# List all pinned threads of a user
@app.route('/message/likes_count', methods=['GET'])
def get_message_likes_count():
    token = request.args.get('token')
    message = request.args.get('message_id')
    return forum_db.get_likes_count(token, message)

# Get messages liked by user
@app.route('/message/liked', methods=['GET'])
def liked_messages():
    token = request.args.get('token')
    return forum_db.list_liked(token)

#==============================================================================
# Notifications
#==============================================================================

# Notify users when forum created
@app.route('/thread/notify', methods=['POST'])
def notify_users_forum():
    info = request.get_json()
    return notification.notify_forum(info['token'],
                                     info['thread_id'], info['course_code'])

# Notify users when an assessment is created
@app.route('/materials/notify', methods=['POST'])
def notify_users_course_material():
    info = request.get_json()
    return notification.notify_course_material(info['token'],
                                          info['filename'], info['course_code'])

#==============================================================================
# Quizzes
#==============================================================================

# Create a new quiz
@app.route('/quiz/create', methods=['POST'])
def create_quiz():
    info = request.get_json()
    return quiz_db.create_quiz(
                                info['token'],
                                info['name'],
                                info['description'],
                                info['due_date'],
                                info['course_code']
                               )

# Fetch all quizzes
@app.route('/quizzes', methods=['GET'])
def get_quizzes():
    token = request.args.get('token')
    course_code = request.args.get('course_code')
    return quiz_db.get_quizzes(token, course_code)

# Fetch single quiz
@app.route('/quiz', methods=['GET'])
def get_quiz():
    token = request.args.get('token')
    quiz_id = request.args.get('quiz_id')
    return quiz_db.get_quiz(token, quiz_id)

# Update the quiz
@app.route('/quiz/update', methods=['PUT'])
def update_quiz():
    info = request.get_json()
    return quiz_db.update_quiz(
                                info['token'],
                                info['quiz_id'],
                                info['name'],
                                info['description'],
                                info['due_date'],
                               )

# Create a new question
@app.route('/question/create', methods=['POST'])
def create_question():
    info = request.get_json()
    return quiz_db.create_question(
                                info['token'],
                                info['description'],
                                info['quiz_id']
                               )

# Delete a question
@app.route('/question/delete', methods=['DELETE'])
def delete_question():
    info = request.get_json()
    return quiz_db.delete_question(
                                info['token'],
                                info['question_id'],
                               )

# Update the quiz
@app.route('/question/update', methods=['PUT'])
def update_question():
    info = request.get_json()
    return quiz_db.update_question(
                                info['token'],
                                info['question_id'],
                                info['description'],
                                info['answers'],
                               )

# Create a new option
@app.route('/option/create', methods=['POST'])
def create_option():
    info = request.get_json()
    return quiz_db.create_option(
                                info['token'],
                                info['description'],
                                info['correct'],
                                info['question_id']
                               )

# Update the quiz
@app.route('/option/update', methods=['PUT'])
def update_option():
    info = request.get_json()
    return quiz_db.update_option(
                                info['token'],
                                info['option_id'],
                                info['description'],
                                info['correct']
                               )

# Answer the question
@app.route('/question/answer', methods=['POST'])
def answer_question():
    info = request.get_json()
    return quiz_db.answer_question(
                                info['token'],
                                info['answers'],
                                info['question_id'],
                                info['user_id']
                               )

# Get the answer for a question
@app.route('/answer/get', methods=['GET'])
def get_answers():
    token = request.args.get('token')
    question_id = request.args.get('question_id')
    user_id = request.args.get('user_id')
    return quiz_db.get_answers(
                                token,
                                question_id,
                                user_id
                               )

# Get the question
@app.route('/question', methods=['GET'])
def get_question():
    token = request.args.get('token')
    question_id = request.args.get('question_id')
    return quiz_db.get_question(
                                token,
                                question_id
                               )

# Get the attempts user made to a quiz
@app.route('/quiz/attempts', methods=['GET'])
def get_attempts():
    token = request.args.get('token')
    user_id = request.args.get('user_id')
    quiz_id = request.args.get('quiz_id')
    return quiz_db.get_attempts(
                                token,
                                user_id,
                                quiz_id
                               )

# Get the attempts user made to a quiz
@app.route('/quiz/mark', methods=['POST'])
def mark_quiz():
    info = request.get_json()
    return quiz_db.mark_quiz(
                                info['token'],
                                info['quiz_id'],
                                info['answerList']
                               )

# Get students quiz marks
@app.route('/student/quiz/mark', methods=['GET'])
def student_quiz_results():
    token = request.args.get('token')
    studentId = request.args.get('studentId')
    return quiz_db.get_student_quiz_results(token, studentId)


#==============================================================================
# DialogFlow Chatbot
#==============================================================================
@app.route('/chatbot/start', methods=['GET', 'POST'])
def chatbotStart():
    session_id = generateSessionID()
    return {'message': startConversion(session_id), 'id': session_id}

@app.route('/chatbot/send', methods=['GET', 'POST'])
def chatbot():
    req = request.get_json()
    return conversation(req['query'], req['session_id'])

if __name__ == "__main__":
    app.run(debug=True)
