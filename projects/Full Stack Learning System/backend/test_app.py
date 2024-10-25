import psycopg2
import config
from db.db_user import Db_user
from db.db_course import Db_course
from db.db_forum import Db_forum
from db.db_file import Db_file
from db.db_assessment import Db_assessment
from db.create_table_queries import queries
from db.db import init_db_command
import requests
import json
from datetime import datetime, timedelta

db = psycopg2.connect(host=config.HOST, port=config.PORT, database=config.DATABASE, user=config.USER, password=config.PASSWORD)

# Setup access to database
user_db = Db_user(db)
course_db = Db_course(db)
forum_db = Db_forum(db)
file_db = Db_file(db)
assessment_db = Db_assessment(db)
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTExODU0NjYxNzMzODk3MjY1MDg3In0.4lu1pzZ66K3y_W9tZnWSrFNlrp9k_p6-5ubmUxQRFTw"

url = 'http://127.0.0.1:5000'
headers = {
    'Content-Type' : 'application/json'
}

def test_new_user():
    data = {
        'user_id' : '111854661733897265087', 
        'name' : '3900W11AYellowFrogs',
        'email' : '3900w11ayellowfrogs@gmail.com'
    }
    res = requests.post(f"{url}/user/add", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'token' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTExODU0NjYxNzMzODk3MjY1MDg3In0.4lu1pzZ66K3y_W9tZnWSrFNlrp9k_p6-5ubmUxQRFTw'}

def test_user_logout():
    data = {
        'token' : token
    }
    res = requests.post(f"{url}/user/logout", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_user_login():
    data = {
        'user_id' : '111854661733897265087', 
        'email' : '3900w11ayellowfrogs@gmail.com'
    }
    res = requests.post(f"{url}/user/login", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'token' : token}

def test_add_lecturer():
    data = {
        'token' : token
    }
    res = requests.post(f"{url}/user/add_lecturer", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_add_student():
    data = {
        'token' : token
    }
    res = requests.post(f"{url}/user/add_student", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_user_avatar():
    data = {
        'token' : token,
        'avatar' : 'imagehere'
    }
    res = requests.put(f"{url}/user/avatar", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_thread_add():
    data = {
        'token' : token,
        'title' : 'Title here',
        'course' : 'COMP1511'
    }
    res = requests.post(f"{url}/thread/add", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'thread_id': 7}

def test_thread_pin():
    data = {
        'token' : token,
        'thread_id' : '5',
    }
    res = requests.post(f"{url}/thread/pin", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_thread_unpin():
    data = {
        'token' : token,
        'thread_id' : '5',
    }
    res = requests.delete(f"{url}/thread/unpin", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_message_add():
    data = {
        'file_name' : ["helloworld.txt"],
        'token' : token,
        'message' : "Hello world",
        "thread" : '5'
    }
    res = requests.post(f"{url}/message/add", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'file_id': 1, 'message_id': 11}

def test_message_pin():
    data = {
        'message_id' : '9',
        'token' : token
    }
    res = requests.post(f"{url}/message/pin", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_message_unpin():
    data = {
        'message_id' : '9',
        'token' : token
    }
    res = requests.post(f"{url}/message/unpin", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_message_like():
    data = {
        'message' : '9',
        'token' : token
    }
    res = requests.post(f"{url}/message/like", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_message_unlike():
    data = {
        'message' : '9',
        'token' : token
    }
    res = requests.delete(f"{url}/message/unlike", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_course_create():
    data = {
        'token' : token,
        'name' : 'Intro to astronomy',
        'code' : 'PHYS1160',
        'description' : 'About astronomy'
    }
    res = requests.post(f"{url}/create/course", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_course_join():
    data = {
        'token' : token,
        'course_code' : 'PHYS1160'
    }
    res = requests.post(f"{url}/course/join", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_create_assessment():
    data = {
        'token' : token,
        'title' : 'Assessment 1',
        'description' : 'Assessment 1 is hard',
        'due_date' : f'{datetime(2025, 1, 1, 12, 30)}',
        'marks' : '100',
        'hidden' : True,
        'course_code' : 'PHYS1160',
        'file_name' : 'Spec1'
    }
    res = requests.post(f"{url}/create/assessment", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'assessment_id' : 9,'file_id': 2}

    assessment_id = res.json()['assessment_id']

    data = {
        'token' : token,
        'hidden' : False,
        'assessment_id' : assessment_id
    }
    res = requests.post(f"{url}/publish/assessment", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

def test_open_assessments():
    data = {
        'token' : token
    }
    res = requests.get(f"{url}/open/assessments", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == [
                            {
                                "asstName": "Assessment 1",
                                "course": "PHYS1160",
                                "due_date": "Wed, 01 Jan 2025 12:30:00 GMT"
                            }
                        ]


def test_results_assessments():
    data = {
        'token' : token
    }
    res = requests.get(f"{url}/assessments/results", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == []

def test_submit_assessment():
    data = {
        'token' : token,
        'assessment' : '1',
        'file_name' : 'SolutionAttempt1'
    }
    res = requests.post(f"{url}/submit/assessment", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'submission_id' : 5, 'file_id': 3}

def test_mark_assessment():
    data = {
        'token' : token,
        'mark' : '85',
        'assessment' : '1',
        'student_id' : '111854661733897265087'
    }
    res = requests.post(f"{url}/mark/assessment", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {}

# def test_course_list():
#     data = {
#         'course_code' : 'COMP1511', 
#         'token' : token
#     }
#     res = requests.get(f"{url}/course/list", params=data, headers=headers)
#     assert res.status_code == 200
#     assert res.json() == {
#                             "assessments": [
#                                 {
#                                 "due_date": "Wed, 01 Jan 2025 12:30:00 GMT",
#                                 "name": "Assessment 1"
#                                 }
#                             ],
#                             "code": "COMP1511",
#                             "description": "Intro Comp",
#                             "lecturers": [
#                                 {
#                                 "user_id": "23456789",
#                                 "user_name": "JoeTeach"
#                                 }
#                             ],
#                             "name": "COmp",
#                             "students": [
#                                 {
#                                 "user_id": "45678901",
#                                 "user_name": "Pete"
#                                 },
#                                 {
#                                 "user_id": "56789012",
#                                 "user_name": "Nam"
#                                 }
#                             ]
#                             }


def test_user_courses():
    data = {
        'token' : token
    }
    res = requests.get(f"{url}/user/courses", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {
                            "student_of": [
                                {
                                "code": "PHYS1160",
                                "description": "About astronomy",
                                "name": "Intro to astronomy"
                                }
                            ],
                            "teaches": [
                                {
                                "code": "PHYS1160",
                                "description": "About astronomy",
                                "name": "Intro to astronomy"
                                }
                            ]
                        }

def test_material_search():
    data = {
        'token' : token,
        'course_code' : 'ELEC1111',
        'search_word' : 'assess'
    }
    res = requests.get(f"{url}/search/material", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {
                            "assessments": [
                                {
                                "assessment_id": 2,
                                "due_date": "Sat, 01 Jan 2022 12:30:00 GMT",
                                "title": "Assessment 2"
                                },
                                {
                                "assessment_id": 3,
                                "due_date": "Sat, 01 Jan 2022 16:30:00 GMT",
                                "title": "Assessment 3"
                                }
                            ],
                            "files": []
                            }

def test_user_islecturer():
    data = {
        'token' : token
    }
    res = requests.get(f"{url}/user/is_lecturer", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'is_lecturer' : True}

def test_user_exists():
    data = {
        'user_id' : '123456789'
    }
    res = requests.get(f"{url}/user/exists", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'exists' : False}

def test_user():
    data = {
        'token' : token
    }
    res = requests.get(f"{url}/user", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'avatar': 'imagehere', 'email': '3900w11ayellowfrogs@gmail.com', 'name': '3900W11AYellowFrogs'}

def test_threads_list():
    data = {
        'token' : token,
        'course_code' : 'PHYS1160'
    }
    res = requests.get(f"{url}/threads/list", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {
                            "pinned_threads": [],
                            "threads": []
                        }

def test_message_list():
    data = {
        'token' : token,
        'thread_id' : '8'
    }
    res = requests.get(f"{url}/message/list", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'Alert': 'Thread does not exist'}

def test_message_likes():
    data = {
        'token' : token,
        'message_id' : '1'
    }
    res = requests.get(f"{url}/message/likes_count", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'count': 0}

def test_message_liked_by_list():
    data = {
        'token' : token
    }
    res = requests.get(f"{url}/message/liked", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == []

def test_quiz_create():
    data = {
        'token' : token,
        'name' : 'Quiz 1',
        'description' : 'Quiz 1 is about quizzes.',
        'open_date' : f'{datetime.now()}',
        'due_date' : f'{datetime.now() + timedelta(hours=1, minutes=30)}',
        'max_duration' : '(0,0,30)',
        'max_attempts' : '1',
        'result_hidden' : True,
        'course_code' : 'COMP1511',
    }
    res = requests.post(f"{url}/quiz/create", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'quiz_id': 3}

    quiz_id = res.json()['quiz_id']
    data = {
        'token' : token,
        'quiz_id' : quiz_id,
        'name' : 'Quiz 1',
        'description' : 'Quiz 1 is about quizzes.',
        'open_date' : f'{datetime.now()}',
        'due_date' : f'{datetime.now() + timedelta(hours=1, minutes=30)}',
        'max_duration' : '(0,0,50)',
        'max_attempts' : '3',
        'result_hidden' : False,
    }
    res = requests.put(f"{url}/quiz/update", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'quiz_id': 3}

def test_question_create():
    data = {
        'token' : token,
        'description' : 'Question 1 is about quizzes.',
        'multiple' : '1',
        'score' : '2',
        'quiz_id' : '3'
    }
    res = requests.post(f"{url}/question/create", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'question_id' : 3}

    question_id = res.json()['question_id']

    data = {
        'token' : token,
        'question_id' : question_id,
        'description' : 'Question 1 is about quizzes.',
        'multiple' : '1',
        'score' : '4',
    }
    res = requests.put(f"{url}/question/update", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'question_id' : 3}

def test_option_create():
    data = {
        'token' : token,
        'description' : 'Option 1',
        'correct' : False,
        'question_id' : '3',
    }
    res = requests.post(f"{url}/option/create", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'option_id': 1}

    option_id = res.json()['option_id']

    data = {
        'token' : token,
        'option_id' : option_id,
        'description' : 'Option 1 is now changes.',
        'correct' : True,
    }
    res = requests.put(f"{url}/option/update", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'option_id' : 1}

def test_question_answer():
    data = {
        'token' : token,
        'answers' : [1, 2],
        'question_id' : '2',
        'user_id' : '34567890'
    }
    res = requests.post(f"{url}/question/answer", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'answer_id': 2}

def test_answer_get():
    data = {
        'token' : token,
        'question_id' : 2,
        'user_id' : 34567890,
    }
    res = requests.get(f"{url}/answer/get", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {
                            "answer_id": 2,
                            "answers": [
                                1,
                                2
                            ]
                        }

# # Working but can't be tested due to changing times/dates
# def test_quiz_get():
#     data = {
#         'token' : token,
#         'quiz_id' : '2'
#     }
#     res = requests.get(f"{url}/quiz/get", params=data, headers=headers)
#     assert res.status_code == 200
#     assert res.json() == {
#                             "created": "Mon, 24 Jul 2023 01:44:52 GMT",
#                             "description": "Quiz 1 is about quizzes.",
#                             "due_date": "Mon, 24 Jul 2023 03:14:52 GMT",
#                             "max_attempts": 3,
#                             "max_duration": "(0,0,50)",
#                             "name": "Quiz 1",
#                             "open_date": "Mon, 24 Jul 2023 01:44:52 GMT",
#                             "questions": [
#                                 {
#                                 "description": "Question 1 is about quizzes.",
#                                 "multiple": True,
#                                 "options": [
#                                     {
#                                     "description": "Option 1 is now changes.",
#                                     "option_id": 1
#                                     }
#                                 ],
#                                 "question_id": 2,
#                                 "score": 4,
#                                 "true_answers": None
#                                 }
#                             ],
#                             "quiz_id": 2,
#                             "result_hidden": False
#                          }


def test_question_get():
    data = {
        'token' : token,
        'question_id' : '3',
    }
    res = requests.get(f"{url}/question/get", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {
                            "description": "Question 1 is about quizzes.",
                            "multiple": True,
                            "options": [{"description": "Option 1 is now changes.", "option_id": 1}],
                            "question_id": 3,
                            "score": 4,
                            "true_answers": None
                        }

def test_quiz_attempts():
    data = {
        'token' : token,
        'user_id' : '34567890',
        'quiz_id' : '2',
    }
    res = requests.get(f"{url}/quiz/attempts", params=data, headers=headers)
    assert res.status_code == 200
    assert res.json() == {'attempts': 0}

def test_question_mark():
    data = {
        'token' : token,
        'user_id' : '34567890',
        'quiz_id' :  '3',
    }
    res = requests.post(f"{url}/quiz/mark", data=json.dumps(data), headers=headers)
    assert res.status_code == 200
    assert res.json() == {'marks': '0 / 4'}