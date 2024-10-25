# from db.db_quiz import *
# from config import *

# from datetime import datetime, timezone, timedelta
# import psycopg2

# # Connect to database
# db = psycopg2.connect(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)
# quiz = Db_quiz(db)

# def testQuiz():
#     now = datetime.now(timezone.utc)
#     open = now + timedelta(hours=1)
#     end = open + timedelta(days=2)
#     res = quiz.create_quiz('Week 2', 'Guess it', open, end, (0, 1, 30), 4, False, 'COMP1511')
#     print(res)

#     res = quiz.update_quiz(res['quiz_id'], 'Week 2', 'No guesses this time', open, end, (0, 4, 30), 1, True)
#     print(res)

# def testQuestion():
#     quiz.create_option('Linear Regression methods can solve classification problems', False, 1)
#     quiz.create_option('Random Forest is an integration of Decision Trees', True, 1)

#     id_1 = quiz.create_question('Choose from the following that is correct:', False, 4, 1)['question_id']
#     quiz.create_option('Linear Regression methods can solve classification problems', False, id_1)
#     quiz.create_option('Random Forest is an integration of Decision Trees', True, id_1)

#     id_2 = quiz.create_question('When dealing with high dimensionalities dataset, it would be better to use:', True, 2, 1)['question_id']
#     quiz.create_option('Linear Regression', False, id_2)
#     quiz.create_option('Support Vector mechine', True, id_2)
#     quiz.create_option('Decision Tree', False, id_2)
#     quiz.create_option('Random Forest', True, id_2)

#     id_3 = quiz.create_question('When dealing with high dimensionalities dataset, it would be better to use:', True, 2, 1)['question_id']
#     quiz.create_option('Linear Regression', False, id_3)
#     quiz.create_option('Support Vector mechine', True, id_3)
#     quiz.create_option('Decision Tree', False, id_3)
#     quiz.create_option('Random Forest', True, id_3)
    
# def testAnswer():
#     quiz.answer_question([2], 1, '1')
#     quiz.answer_question([4], 2, '1')
#     quiz.answer_question([6,8], 3, '1')
#     quiz.answer_question([2], 4, '1')

# def testMarking():
#     print(quiz.get_attempts('1', 1))
#     print(quiz.mark_quiz('1', 1))
#     print(quiz.get_attempts('1', 1))
#     print(quiz.mark_quiz('1', 1))
#     print(quiz.get_attempts('1', 1))

# def testGET():
#     print(quiz.get_quiz(1))

# testQuiz()
# testQuestion()
# testAnswer()
# testMarking()