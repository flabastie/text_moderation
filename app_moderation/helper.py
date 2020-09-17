import sqlite3
import traceback
import config

DB_PATH = config.db_path

def add_to_list(comment):

    try:
        conn = sqlite3.connect(DB_PATH)

        # Once a connection has been established, we use the cursor
        # object to execute queries
        c = conn.cursor()
        print (comment)
        # Keep the initial status as Not Started
        c.execute("insert into comments values ('{value}');".format(value = comment))

        # We commit to save the change
        conn.commit()
        return {"comment": comment}

    except Exception as e:
        # print('Error: ', e)
        print(traceback.format_exc())
        return None

def get_list():

    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        posts = c.execute('SELECT * FROM comments ORDER BY rowid desc limit 5').fetchall()
        c.close()
        return posts
        
    except Exception as e:
        # print('Error: ', e)
        print(traceback.format_exc())
        return None