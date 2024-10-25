# Contains the database initializing functions
# Also load the database with 'dummy' data

import psycopg2
from db.db_user import Db_user
from db.create_table_queries import queries
import config
from db.dummy_data import dummy_queries
from db.delete_table_queries import drop_queries

# Init the database by creating all the tables and
# adding the dummy data
def init_db_command(db):

    # Drop all tables
    cur = db.cursor()
    for query in drop_queries:
        cur.execute(query)
    db.commit()

    # Create all tables
    for query in queries:
        cur.execute(query)
    db.commit()

    # Add dummy data to tables
    for query in dummy_queries:
        cur.execute(query)
    db.commit()
    cur.close()