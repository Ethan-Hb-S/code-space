import db.token_handler
from datetime import datetime, timezone
from db.input_checks import does_course_exist, does_message_exist, does_question_exist, does_quiz_exist

class Db_quiz():
    def __init__(self, db):
        self.db = db
    
    # Create a new quiz
    def create_quiz(self, token, name, description, due_date, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if course exists        
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        cur = self.db.cursor()

        qry = """insert into quizzes(name, description, due_date, course)
                values(%s, %s, %s, %s)
                returning quiz_id;"""
        cur.execute(qry, [name, description, due_date, course_code])

        quiz_id = cur.fetchone()[0]
        self.db.commit()
        cur.close()
        return { "quiz_id" : quiz_id }
    
    # Update a quiz
    # !Note that, both of the created time and course code will not be able to update
    def update_quiz(self, token, quiz_id, name, description, due_date):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if quiz exists        
        if not does_quiz_exist(self.db, quiz_id):
            return {'Alert' : 'Quiz does not exist'}

        cur = self.db.cursor()

        qry = """update quizzes set name = %s, description = %s, 
                due_date = %s
                where quiz_id = %s;"""
        cur.execute(qry, [name, description, due_date, quiz_id])

        self.db.commit()
        cur.close()
        return { "quiz_id" : quiz_id }

    # Delete question
    def delete_question(self, token, question_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}
        
        # Check if question exists
        if not does_question_exist(self.db, question_id):
            return {'Alert' : 'Question does not exist'}
        
        cur = self.db.cursor()

        qry = """delete from answers where question = %s;"""
        cur.execute(qry, [question_id])

        qry = """delete from questions where question_id = %s;"""
        cur.execute(qry, [question_id])

        self.db.commit()
        cur.close()

        return {}


    # Create a question for a quiz
    def create_question(self, token, description, quiz_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if quiz exists        
        if not does_quiz_exist(self.db, quiz_id):
            return {'Alert' : 'Quiz does not exist'}

        cur = self.db.cursor()

        qry = """insert into questions(description, quiz)
                values(%s, %s) 
                returning question_id;"""
        cur.execute(qry, [description, quiz_id])

        question_id = cur.fetchone()[0]

        qry = """insert into answers(is_correct, answer_string, question) values(false, 'A', %s)"""
        cur.execute(qry, [question_id])

        qry = """insert into answers(is_correct, answer_string, question) values(true, 'B', %s)"""
        cur.execute(qry, [question_id])

        qry = """insert into answers(is_correct, answer_string, question) values(false, 'C', %s)"""
        cur.execute(qry, [question_id])
        
        qry = """insert into answers(is_correct, answer_string, question) values(false, 'D', %s)"""
        cur.execute(qry, [question_id])

        self.db.commit()
        cur.close()
        return { "question_id" : question_id }
    
    # Update the question
    def update_question(self, token, question_id, description, answers):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if question exists        
        if not does_question_exist(self.db, question_id):
            return {'Alert' : 'Question does not exist'}

        cur = self.db.cursor()

        qry = """update questions set description = %s where question_id = %s;"""
        cur.execute(qry, [description, question_id])

        self.db.commit()
        cur.close()

        self.update_answers(answers)

        return { "question_id" : question_id }
    
    # Update answers
    def update_answers(self, answers):
        cur = self.db.cursor()
        for answer in answers:
            qry = """update answers set answer_string = %s, is_correct = %s where answer_id = %s"""
            cur.execute(qry, [answer['answer_string'], answer['is_correct'], answer['answer_id']])

    # Update true answers in a question
    # (Won't be used in endpoints)
    def update_trueAnswers(self, question_id, option_id):
        cur = self.db.cursor()

        qry = """update questions set description = %s, multiple = %s
                where question_id = %s;"""
        cur.execute(qry, [option_id, question_id])

        self.db.commit()
        cur.close()
        return
    
    # Create a new option for a question
    def create_option(self, token, description, correct, question_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if question exists        
        if not does_question_exist(self.db, question_id):
            return {'Alert' : 'Question does not exist'}

        cur = self.db.cursor()

        qry = """insert into options(description, correct, question)
                values(%s, %s, %s) 
                returning option_id;"""
        cur.execute(qry, [description, correct, question_id])
        option_id = cur.fetchone()[0]

        if correct:
            trueAns = self.get_question(question_id)['true_answers']
            if trueAns == None: trueAns = []
            trueAns.append(option_id)
            qry = """update Questions set true_answers = %s
                    where question_id = %s;"""
            cur.execute(qry, [trueAns, question_id])

        self.db.commit()
        cur.close()
        return { "option_id" : option_id }
    
    # Update the option
    def update_option(self, token, option_id, description, correct):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}
        
        cur = self.db.cursor()

        qry = """update options set description = %s, correct = %s
                where option_id = %s;"""
        cur.execute(qry, [description, correct, option_id])

        self.db.commit()
        cur.close()
        return { "option_id" : option_id }
    
    # Create or Update the answer set to the question for a student(user)
    def answer_question(self, token, answers: list, question_id, user_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if question exists        
        if not does_question_exist(self.db, question_id):
            return {'Alert' : 'Question does not exists'}

        ans = self.get_answers(token, question_id, user_id)['answer_id']
        
        cur = self.db.cursor()
        if ans == None:
            # If id is None, the user must be the first time doing this question
            # So need to create a new answer row to database
            qry = """insert into answers(selections, question, user_id)
                    values(%s, %s, %s) 
                    returning answer_id;"""
        else:
            # Otherwise just simply replace the old answer with the new
            qry = """update answers set selections = %s
                    where question = %s and user_id = %s
                    returning answer_id;"""
        
        cur.execute(qry, [answers, question_id, user_id])
        answer_id = cur.fetchone()[0]

        self.db.commit()
        cur.close()
        return { 'answer_id' : answer_id }
    
    # Get the answer set of a student(user) by question and user ID
    def get_answers(self, token, question_id, user_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if question exists        
        if not does_question_exist(self.db, question_id):
            return {'Alert' : 'Question does not exist'}

        cur = self.db.cursor()

        qry = """select * from Answers a
                where a.question = %s and a.user_id = %s;"""
        cur.execute(qry, [question_id, user_id])

        res = cur.fetchone()
        id, answers = None, None
        if res != None:
            id, answers = res[0], res[1]
        cur.close()
        return { 
                "answer_id" : id,
                "answers" : answers
                }
    
    # Get the whole quiz object
    def get_quiz(self, token, quiz_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}
        
        # Check if quiz exists        
        if not does_quiz_exist(self.db, quiz_id):
            return {'Alert' : 'Quiz does not exist'}

        cur = self.db.cursor()

        qry = """select * from Quizzes where quiz_id = %s;"""
        cur.execute(qry, [quiz_id])
        res = cur.fetchone()
        id, name, description, due, course = res
        # get all ids of questions belong to the quiz
        qry = """select * from Questions where quiz = %s;"""
        cur.execute(qry, [quiz_id])
        res = cur.fetchall()

        questions = []
        for i in res:
            questions.append(self.get_question(token, i[0]))

        cur.close()
        return { 
                "quiz_id" : id,
                "name" : name,
                "description" : description,
                "due_date" : due,
                "questions" : questions
                }
    
    # Get students quiz marks
    def get_student_quiz_results(self, token, studentId):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        cur = self.db.cursor()
        qry = """select q.name, m.marks
                from quiz_marks m
                join quizzes q on q.quiz_id = m.quiz
                where user_id = %s;"""
        cur.execute(qry, [studentId])

        res = []
        for mark in cur.fetchall():
            res.append({'asstName': mark[0], 'mark': mark[1][0], 'outOf': mark[1][1:], 'quiz': True})
        cur.close()
        return res

    # Get a question and all its data
    def get_question(self, token, question_id):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}
        
        # Check if question exists        
        if not does_question_exist(self.db, question_id):
            return {'Alert' : 'Question does not exist'}

        cur = self.db.cursor()

        qry = """select * from Questions where question_id = %s;"""
        cur.execute(qry, [question_id])
        res = cur.fetchone()
        id, description = res[0], res[1]

        # get all options in it
        qry = """select * from Answers where question = %s;"""
        cur.execute(qry, [question_id])
        res = cur.fetchall()
        answers = []
        for i in res:
            answers.append( {
                            "answer_id" : i[0],
                            "is_correct" : i[1],
                            "answer_string" : i[2],
            } )

        cur.close()
        return { 
                "question_id" : id,
                "description" : description,
                "answers" : answers,
                }
    
    # Get the options
    def get_option(self, option_id):
        cur = self.db.cursor()

        qry = """select * from Options where option_id = %s;"""
        cur.execute(qry, [option_id])

        res = cur.fetchone()
        id, description = res[0], res[1], res[2]
        cur.close()
        return { 
                "option_id" : id,
                "description" : description
                }
    
    # Get the attempts that the user have already did to the quiz
    def get_attempts(self, token, user, quiz):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        # Check if quiz exists        
        if not does_quiz_exist(self.db, quiz):
            return {'Alert' : 'Quiz does not exist'}

        cur = self.db.cursor()

        qry = """select * from Quiz_marks
                where quiz = %s and user_id = %s;"""
        cur.execute(qry, [quiz, user])

        res = cur.fetchall()
        cur.close()
        return { 'attempts' : len(res) }
    
    # Get a quiz marked based on the current answers user made
    def mark_quiz(self, token, quiz, answerList):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}
        user = token_data['user_id']

        # Check if quiz exists        
        if not does_quiz_exist(self.db, quiz):
            return {'Alert' : 'Quiz does not exist'}

        questions = self.get_quiz(token, quiz)['questions']
        achieved_marks = 0
        total_marks = 0

        for ans in answerList.values():
            if self.marked_correct(ans):
                achieved_marks += 1
            total_marks += 1

        # The final marks will be the ratio of achieved marks and total marks
        marks = f'{achieved_marks} / {total_marks}'
        cur = self.db.cursor()

        qry = """insert into Quiz_marks(marks, quiz, user_id)
                values(%s, %s, %s);"""
        cur.execute(qry, [marks, quiz, user])

        self.db.commit()
        cur.close()
        return { "marks" : marks }
    
    # Get marked for a single question
    def marked_correct(self, answers: list) -> bool:
        if len(answers) == 0:
            return False
        
        cur = self.db.cursor()

        for i in answers:
            qry = """select is_correct from Answers where answer_id = %s;"""
            cur.execute(qry, [i])
            correct = cur.fetchone()[0]
            if not correct: return False
        
        return True
    
    # Get all quizzes
    def get_quizzes(self, token, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return {'Alert' : 'Invalid token'}

        quizzes = []
        cur = self.db.cursor()
        qry = """select quiz_id, name, description, due_date from Quizzes
                where course = %s;"""
        cur.execute(qry, [course_code])
        for each in cur.fetchall():
            quizzes.append({
                'quiz_id': each[0],
                'name': each[1],
                'description': each[2],
                'due_date': each[3]
            })
        self.db.commit()
        cur.close()

        return { 'quizzes': quizzes }