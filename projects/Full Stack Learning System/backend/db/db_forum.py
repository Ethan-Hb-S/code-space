import json
import db.token_handler
from datetime import datetime, timezone
from db.db_file import Db_file
from db.input_checks import does_course_exist, does_thread_exist, does_message_exist

class Db_forum():
    def __init__(self, db):
        self.db = db
        self.file = Db_file(db)

    # Add a new thread to the course
    def add_thread(self, token, title, course):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if course exists        
        if not does_course_exist(self.db, course):
            return {'Alert' : 'Course does not exist'}

        cur = self.db.cursor()

        created = datetime.now(timezone.utc)
        qry = """insert into threads(thread_title, created, course, user_id)
                values(%s, %s, %s, %s)
                returning thread_id;"""
        cur.execute(qry, [title, created, course, token_data['user_id']])
        id = cur.fetchone()[0]
        self.db.commit()

        cur.close()
        return { 'thread_id' : id }
    
    # List the threads in a certain course
    def list_threads(self, token, course_code):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if course exists        
        if not does_course_exist(self.db, course_code):
            return {'Alert' : 'Course does not exist'}

        cur = self.db.cursor()

        # This query gets all of the threads that are NOT pinned by the current user
        qry = """(select t.thread_id, t.thread_title, t.created, 
                  t.user_id, u.name, u.avatar
                    from threads t join users u on u.user_id = t.user_id 
                    where t.course = %s)
                EXCEPT 
                 (select t.thread_id, t.thread_title, t.created,
                  t.user_id, u.name, u.avatar
                    from threads t join pinned_threads_by p on p.thread = t.thread_id
                    join users u on u.user_id = t.user_id
                    where t.course = %s and p.user_id = %s)
                order by thread_id"""
        cur.execute(qry, [course_code, course_code, token_data['user_id']])
        res = cur.fetchall()

        threads = []
        for i in res:
            id, title, created = i[0], i[1], i[2]
            author, author_name, author_avatar = i[3], i[4], i[5]

            threads.append({
                'thread_id': id,
                'thread_title': title,
                'created': created,
                'author_id': author,
                'author_name' : author_name,
                'author_avatar' : author_avatar
            })

        cur.close()
        # This query gets all of the threads that ARE pinned by the current user
        pinned_threads = self.list_pinned_threads(token_data['user_id'], course_code)
        return {'threads' : threads, 'pinned_threads' : pinned_threads}
    
    # Add a new message
    def add_message(self, token, message, thread, file_name):
        token_data = db.token_handler.token_decoder(token)
        
        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        cur = self.db.cursor()

        created = datetime.now(timezone.utc)
        qry = """insert into messages(message, created, thread, user_id)
                values(%s, %s, %s, %s)
                returning message_id;"""
        cur.execute(qry, [message, created, thread, token_data['user_id']])
        id = cur.fetchone()[0]
        self.db.commit()

        file_id = None
        if file_name:
            for name in file_name:
                file_id = self.file.create_file(token, name, None, id, None)['file_id']

        cur.close()
        # Will return file id if message contains any files
        return { 'message_id' : id, 'file_id' : file_id }

    # List the messages in a certain thread
    def list_messages(self, token, thread):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if thread exists        
        if not does_thread_exist(self.db, thread):
            return {'Alert' : 'Thread does not exist'}

        cur = self.db.cursor()

        # This query gets all of the messages that are NOT pinned by the current user
        qry = """(select m.message_id, m.message, m.created, m.user_id, 
                    f.file_id, f.name, u.name, u.avatar from messages m
                    left join files f on f.message = m.message_id 
                    join users u on u.user_id = m.user_id
                    where m.thread = %s order by m.message_id) 
                 EXCEPT                                                        
                 (select m.message_id, m.message, m.created, 
                  m.user_id, f.file_id, f.name, 
                  u.name, u.avatar from messages m
                    join users u on u.user_id = m.user_id
                    left join files f on f.message = m.message_id 
                    left join threads t on t.thread_id = m.thread 
                    left join pinned_messages_by p on m.message_id = p.message 
                    where t.thread_id = %s and p.user_id = %s order by m.message_id)
                 order by message_id;"""        
        cur.execute(qry, [thread, thread, token_data['user_id']])
        res = cur.fetchall()

        messages = {}
        # Format the result into JSON
        for i in res:
            id, message, created, uid, f_id, f_name, u_name, u_avatar = i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]
            if id in messages:
                messages[id]['files'].append({'file_id': f_id, 
                                              'name': f_name})
            else:
                messages[id] = {'message_id': id, 
                                'message': message, 
                                'created': created, 
                                'files': [{'file_id': f_id, 
                                           'name': f_name}],
                                'author_id' : uid, 
                                'author_name' : u_name,
                                'author_avatar' : u_avatar}

        cur.close()

        # This query gets all of the messages that ARE pinned by the current user
        pinned_messages = self.list_pinned_messages(token_data['user_id'], thread)
        return {'pinned_messages' : pinned_messages, 'messages' : messages}
    
    # Let the current user pin a message
    def pin_message(self, token, message):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if message exists        
        if not does_message_exist(self.db, message):
            return {'Alert' : 'Message does not exist'}

        cur = self.db.cursor()

        qry = """insert into pinned_messages_by(message, user_id)
                 values(%s, %s);"""
        cur.execute(qry, [message, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Let the current user unpin a message
    def unpin_message(self, token, message):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if message exists        
        if not does_message_exist(self.db, message):
            return {'Alert' : 'Message does not exist'}

        cur = self.db.cursor()

        qry = """delete from pinned_messages_by
                 where message = %s and user_id = %s;"""
        cur.execute(qry, [message, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Let the current user pin a thread
    def pin_thread(self, token, thread):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if thread exists        
        if not does_thread_exist(self.db, thread):
            return {'Alert' : 'Thread does not exist'}

        cur = self.db.cursor()

        qry = """insert into pinned_threads_by(thread, user_id)
                 values(%s, %s);"""
        cur.execute(qry, [thread, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Let the current user unpin a thread
    def unpin_thread(self, token, thread):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if thread exists        
        if not does_thread_exist(self.db, thread):
            return {'Alert' : 'Thread does not exist'}

        cur = self.db.cursor()

        qry = """delete from pinned_threads_by
                 where thread = %s and user_id = %s;"""
        cur.execute(qry, [thread, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Get a list of all pinned messages by the user, this is used internally only
    def list_pinned_messages(self, user_id, thread_id):
        cur = self.db.cursor()

        qry = """select m.message_id, m.message, m.created, m.user_id,
                f.file_id, f.name, u.name, u.avatar from messages m
                    join users u on u.user_id = m.user_id
                    left join files f on f.message = m.message_id
                    left join threads t on t.thread_id = m.thread 
                    left join pinned_messages_by p on m.message_id = p.message 
                    where t.thread_id = %s and p.user_id = %s order by m.message_id"""
        cur.execute(qry, [thread_id, user_id])
        res = cur.fetchall()

        messages = []
        for i in res:
            id, message, created, uid, f_id, f_name, u_name, u_avatar = i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]
            messages.append({'message_id': id, 
                            'message': message, 
                            'created': created, 
                            'files': [{'file_id': f_id, 'name': f_name}],
                            'author_id' : uid, 
                            'author_name' : u_name,
                            'author_avatar' : u_avatar})

        cur.close()
        return messages

    # Get a list of all pinned threads by the user, this is used internally only
    def list_pinned_threads(self, user_id, course_code):
        cur = self.db.cursor()

        qry = """select t.thread_id, t.thread_title, t.created, t.user_id, 
                u.name, u.avatar from threads t 
                    join courses f on t.course = f.course_code 
                    join pinned_threads_by p on t.thread_id = p.thread 
                    join users u on u.user_id = t.user_id 
                where p.user_id = %s and f.course_code = %s;"""
        cur.execute(qry, [user_id, course_code])
        res = cur.fetchall()

        threads = []
        for i in res:
            threads.append({'thread_id':i[0], 'thread_title':i[1], 
                            'created':i[2], 'author_id':i[3],
                            'author_name':i[4], 'author_avatar':i[5]})

        cur.close()
        return threads

    # Let a user like a particular message
    def like_message(self, token, message):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if message exists        
        if not does_message_exist(self.db, message):
            return {'Alert' : 'Message does not exist'}

        cur = self.db.cursor()

        qry = """insert into liked_by(message, user_id) values(%s, %s);"""
        cur.execute(qry, [message, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}

    # Let a user unlike a particular message
    def unlike_message(self, token, message):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data

        # Check if message exists        
        if not does_message_exist(self.db, message):
            return {'Alert' : 'Message does not exist'}

        cur = self.db.cursor()

        qry = """delete from liked_by where message = %s and user_id = %s;"""
        cur.execute(qry, [message, token_data['user_id']])

        self.db.commit()
        cur.close()
        return {}
    
    # Get the likes count of a particular message
    def get_likes_count(self, token, message):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        # Check if message exists        
        if not does_message_exist(self.db, message):
            return {'Alert' : 'Message does not exist'}

        cur = self.db.cursor()

        qry = """select count(*) from liked_by where message = %s"""
        cur.execute(qry, [message])
        count = cur.fetchone()[0]

        cur.close()
        return {'count' : count}
    
    # List all the liked messages of a user
    def list_liked(self, token):
        token_data = db.token_handler.token_decoder(token)

        # If invalid token
        if 'user_id' not in token_data:
            return token_data
        
        cur = self.db.cursor()

        qry = """select * from liked_by where user_id = %s;"""
        cur.execute(qry, [token_data['user_id']])
        res = cur.fetchall()

        messages_liked = []
        for i in res:
            messages_liked.append( i[0] )

        cur.close()
        return messages_liked