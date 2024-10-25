# This file contains the tables for the database

queries = (
    """ create domain MarkRange as
        integer check (value >= 0 AND value <= 100
    )""",
    """ create type Duration as (
        days integer,
        hours integer,
        minutes integer
    )""",
    """ create table if not exists Users (
        user_id varchar(60) not null,
        name varchar(60) not null,
        email varchar(120) not null,
        token text,
        avatar text,
        primary key (user_id)
    )""",
    """ create table if not exists Courses (
        course_code varchar(8) not null,
        name varchar(120) not null,
        description text not null,
        primary key (course_code)
    )""",
    """create table if not exists Assessments (
        assessment_id serial,
        title varchar(256) not null,
        description text not null,
        due_date timestamp,
        marks integer,
        hidden boolean not null,
        course varchar(8) not null references Courses(course_code),
        primary key (assessment_id)
    )""",
    """ create table if not exists Quizzes (
        quiz_id serial,
        name varchar(256) not null,
        description text,
        due_date timestamp,
        course varchar(8) not null references Courses(course_code),
        primary key (quiz_id)
    )""",
    """ create table if not exists Questions (
        question_id serial,
        description text not null,
        quiz integer not null references Quizzes(quiz_id),
        primary key (question_id)
    )""",
    """ create table if not exists Answers (
        answer_id serial,
        is_correct boolean not null,
        answer_string text not null,
        question integer not null references Questions(question_id),
        primary key (answer_id)
    )""",
    """ create table if not exists Quiz_marks (
        id serial,
        marks text not null,
        quiz integer not null references Quizzes(quiz_id),
        user_id varchar(60) not null references Users(user_id),
        primary key (id)
    )""",
    """ create table if not exists Files (
        file_id serial,
        name varchar(256) not null,
        created timestamp not null,
        course varchar(8) references Courses(course_code),
        question integer references Questions(question_id),
        assessment integer references Assessments(assessment_id),
        primary key (file_id)
    )""",
    """ create table if not exists Threads (
        thread_id serial,
        thread_title varchar(256) not null,
        created timestamp not null,
        course varchar(8) not null references Courses(course_code),
        user_id varchar(60) not null references Users(user_id),
        primary key (thread_id)
    )""",
    """ create table if not exists Messages (
        message_id serial,
        message text,
        created timestamp not null,
        thread integer not null references Threads(thread_id),
        user_id varchar(60) not null references Users(user_id),
        primary key (message_id)
    )""",
    """ alter table Files add message integer references Messages(message_id)
    """,
    """ create table if not exists Students (
        student_id varchar(60) references Users(user_id),
        primary key (student_id)
    )""",
    """ create table if not exists Lecturers (
        lecturer_id varchar(60) references Users(user_id),
        primary key (lecturer_id)
    )""",
    """create table if not exists Asst_submissions (
        submission_id serial,
        submission_date timestamp,
        mark integer,
        student_id varchar(60) not null references Students(student_id),
        assessment_id integer not null references Assessments(assessment_id),
        primary key (submission_id)
    )""",
    """ alter table Files add asst_submission integer references Asst_submissions(submission_id)
    """,
    """ create table if not exists Enrolled_in (
        student varchar(60) references Students(student_id),
        course varchar(8) references Courses(course_code),
        primary key (student, course)
    )""",
    """ create table if not exists Teaches (
        lecturer varchar(60) references Lecturers(lecturer_id),
        course varchar(8) references Courses(course_code),
        primary key (lecturer, course)
    )""",
    """ create table if not exists Gets_assessed (
        student varchar(60) not null references Students(student_id),
        assessment integer not null references Assessments(assessment_id),
        mark MarkRange,
        primary key (student, assessment)
    )""",
    """ create table if not exists Liked_by (
        message integer not null references Messages(message_id),
        user_id varchar(60) not null references Users(user_id),
        primary key (message, user_id)
    )""",
    """ create table if not exists Pinned_messages_by (
        message integer not null references Messages(message_id),
        user_id varchar(60) not null references Users(user_id),
        primary key (message, user_id)
    )""",
    """ create table if not exists Pinned_threads_by (
        thread integer not null references Threads(thread_id),
        user_id varchar(60) not null references Users(user_id),
        primary key (thread, user_id)
    )""",
    """ create table if not exists Zoom_meetings (
        zoom_id serial,
        zoom_url text not null,
        status text,
        start_time timestamp,
        zoom_password text,
        primary key (zoom_id)
    )""",
    """ create table if not exists Zoom_per_class (
        course varchar(8) not null references Courses(course_code),
        zoom_id integer not null references Zoom_meetings(zoom_id),
        primary key (course, zoom_id)
    )"""
)