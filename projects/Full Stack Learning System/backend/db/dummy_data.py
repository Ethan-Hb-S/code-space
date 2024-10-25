# File that contains dummy data

from datetime import datetime, timezone, timedelta

created = datetime(2022, 1, 1, 12, 30)

dummy_queries = (
    # Create some users
    """insert into users(user_id, name, email) values('12345678', 'JoeTeacher', 'andrewawesome760@gmail.com');""",
    """insert into users(user_id, name, email) values('23456789', 'TimTeacher', '201exultantpendulum@gmail.com');""",
    """insert into users(user_id, name, email) values('34567890', 'Pete', 'andrewawesome760@gmail.com');""",
    """insert into users(user_id, name, email) values('45678901', 'Nam', '201exultantpendulum@gmail.com');""",
    """insert into users(user_id, name, email) values('67890123', 'Kai', '201exultantpendulum@gmail.com');""",
    """insert into users(user_id, name, email) values('78901234', 'yelofrTeacher', 'lol@gmail.com');""",
    """insert into users(user_id, name, email) values('97265087', '3900W11AYellowFrogs', '3900w11ayellowfrogs@gmail.com');""",
    """insert into users(user_id, name, email) values('26566017', 'team4 comp1531', 'team4comp1531@gmail.com');""",

    # Assign them as teachers or students
    """insert into students(student_id) values('34567890') returning student_id;""",
    """insert into students(student_id) values('45678901') returning student_id;""",
    """insert into students(student_id) values('67890123') returning student_id;""",
    """insert into students(student_id) values('26566017') returning student_id;""",
    """insert into lecturers(lecturer_id) values('12345678') returning lecturer_id;""",
    """insert into lecturers(lecturer_id) values('23456789') returning lecturer_id;""",
    """insert into lecturers(lecturer_id) values('78901234') returning lecturer_id;""",
    """insert into lecturers(lecturer_id) values('97265087') returning lecturer_id;""",

    # Create some courses
    """insert into courses(course_code, name, description) values('COMP1511', 'Comp Sci', 'Intro Comp');""",
    """insert into courses(course_code, name, description) values('ELEC1111', 'Elec Eng', 'Intro Elec');""",
    """insert into courses(course_code, name, description) values('PHYS1131', 'Physics', 'Intro Physics');""",
    """insert into courses(course_code, name, description) values('MATH1141', 'Maths', 'Intro Maths');""",

    # Enroll students into courses
    """insert into enrolled_in(student, course) values('34567890', 'COMP1511');""",
    """insert into enrolled_in(student, course) values('45678901', 'COMP1511');""",
    """insert into enrolled_in(student, course) values('45678901', 'ELEC1111');""",
    """insert into enrolled_in(student, course) values('67890123', 'ELEC1111');""",
    """insert into enrolled_in(student, course) values('26566017', 'ELEC1111');""",
    """insert into enrolled_in(student, course) values('26566017', 'MATH1141');""",
    """insert into enrolled_in(student, course) values('26566017', 'COMP1511');""",
    """insert into enrolled_in(student, course) values('26566017', 'PHYS1131');""",

    # Assign teachers to course
    """insert into teaches(lecturer, course) values('12345678', 'COMP1511');""",
    """insert into teaches(lecturer, course) values('23456789', 'ELEC1111');""",
    """insert into teaches(lecturer, course) values('78901234', 'ELEC1111');""",
    """insert into teaches(lecturer, course) values('97265087', 'PHYS1131');""",
    """insert into teaches(lecturer, course) values('97265087', 'MATH1141');""",    
    """insert into teaches(lecturer, course) values('97265087', 'ELEC1111');""",    
    """insert into teaches(lecturer, course) values('97265087', 'COMP1511');""",    

    # Create some threads and messages in those threads
    f'''insert into threads(thread_title, created, course, user_id) values('Week 1 Q1', '{created}', 'COMP1511', '12345678');''',
    f'''insert into threads(thread_title, created, course, user_id) values('Week 2 Q2', '{created}', 'COMP1511', '34567890');''',
    f'''insert into threads(thread_title, created, course, user_id) values('Week 3 Q3', '{created}', 'ELEC1111', '67890123');''',
    f'''insert into threads(thread_title, created, course, user_id) values('Week 4 Q4', '{created}', 'ELEC1111', '23456789');''',
    f'''insert into threads(thread_title, created, course, user_id) values('A question...', '{created}', 'PHYS1131', '26566017');''',
    f'''insert into threads(thread_title, created, course, user_id) values('Another question...', '{created}', 'MATH1141', '26566017');''',

    f'''insert into messages(message, created, thread, user_id) values('No idea', '{created}', '1', '34567890');''',
    f'''insert into messages(message, created, thread, user_id) values('Hi', '{created}', '1', '45678901');''',
    f'''insert into messages(message, created, thread, user_id) values('Hello', '{created}', '1', '45678901');''',
    f'''insert into messages(message, created, thread, user_id) values('Hey', '{created}', '2', '34567890');''',
    f'''insert into messages(message, created, thread, user_id) values('Bye', '{created}', '2', '12345678');''',
    f'''insert into messages(message, created, thread, user_id) values('Help', '{created}', '3', '67890123');''',
    f'''insert into messages(message, created, thread, user_id) values('Later', '{created}', '4', '23456789');''',
    f'''insert into messages(message, created, thread, user_id) values('Help', '{created}', '4', '67890123');''',
    f'''insert into messages(message, created, thread, user_id) values('An answer...', '{created}', '5', '97265087');''',
    f'''insert into messages(message, created, thread, user_id) values('Another answer...', '{created}', '6', '97265087');''',

    '''insert into pinned_threads_by(thread, user_id) values('1', '34567890');''',
    '''insert into pinned_threads_by(thread, user_id) values('2', '23456789');''',
    '''insert into pinned_threads_by(thread, user_id) values('2', '34567890');''',
    '''insert into pinned_messages_by(message, user_id) values('1', '34567890');''',
    '''insert into pinned_messages_by(message, user_id) values('2', '23456789');''',
    '''insert into pinned_messages_by(message, user_id) values('2', '34567890');''',

    # f'''insert into files(name, created, message) values('file_1', '{created}', '1');''',
    # f'''insert into files(name, created, message) values('file_2', '{created}', '3');''',
    # f'''insert into files(name, created, message) values('file_3', '{created}', '3');''',
    # f'''insert into files(name, created, course) values('file_4', '{created}', 'ELEC1111');''',
    # f'''insert into files(name, created, course) values('file_5', '{created}', 'ELEC1111');''',
    # f'''insert into files(name, created, course) values('file_6', '{created}', 'COMP1511');''',
    # f'''insert into files(name, created, course) values('assessment_file', '{created}', 'ELEC1111');''',
    # f'''insert into files(name, created, course) values('assessment_file', '{created}', 'COMP1511');''',

    # f'''insert into quizzes(name, description, due_date, course) values('Week 1', 'Content based on lec 1', '{created}', 'COMP1511');''',
    # f'''insert into quizzes(name, description, due_date, course) values('Week 1', 'Content based on lec 2', '{created}', 'ELEC1111');''',
    # '''insert into questions(description, quiz) values('Choose the incorrect statement of following:', '1');''',
    # '''insert into questions(description, quiz) values('Choose the correct statement of following:', '2');''',

    # """insert into answers(is_correct, answer_string, question) values('true', 'MyAnswer', '1');""",

    # Create some assessments
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 1', 'Assessment 1 is the assessment 1', '{datetime(2025, 1, 1, 12, 30)}', '10', 'false', 'COMP1511');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 2', 'Assessment 2 is the assessment 2', '{datetime(2022, 1, 1, 12, 30)}', '5', 'false', 'ELEC1111');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 3', 'Assessment 3 is the assessment 3', '{created + timedelta(hours=4)}', '15', 'false', 'ELEC1111');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 1', 'Assessment 1 is the assessment 1', '{datetime(2021, 1, 1, 12, 30)}', '10', 'false', 'PHYS1131');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 2-3', 'An assessment...', '{datetime(2023, 1, 1, 12, 30)}', '50', 'false', 'MATH1141');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 3-3', 'Another assessment...', '{datetime(2024, 1, 1, 12, 30)}', '100', 'false', 'MATH1141');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 2-3', 'An phys assessment...', '{datetime(2022, 1, 1, 12, 30)}', '500', 'false', 'PHYS1131');""",
    f"""insert into assessments(title, description, due_date, marks, hidden, course) values('Assessment 3-3', 'Another phys assessment...', '{datetime(2024, 1, 1, 12, 30)}', '1000', 'false', 'PHYS1131');""",

    # Students who have submitted
    f"""insert into asst_submissions(submission_date, mark, student_id, assessment_id) values('{created}', '10', '34567890', '1')""",
    f"""insert into asst_submissions(submission_date, mark, student_id, assessment_id) values('{created + timedelta(hours=3)}', '5', '67890123', '2')""",
    f"""insert into asst_submissions(submission_date, mark, student_id, assessment_id) values('{datetime(2021, 1, 1, 12, 30)}', '10', '26566017', '5')""",
    f"""insert into asst_submissions(submission_date, mark, student_id, assessment_id) values('{datetime(2021, 1, 1, 12, 30)}', '34', '26566017', '7')""",

    # More files
    # f'''insert into files(name, created, question) values('file_7', '{created}', '1');''',
    # f'''insert into files(name, created, question) values('file_8', '{created}', '2');''',
    # f'''insert into files(name, created, assessment) values('file_9', '{created}', '1');''',
    # f'''insert into files(name, created, assessment) values('file_10', '{created}', '2');''',

)