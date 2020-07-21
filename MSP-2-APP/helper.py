import sqlite3
import traceback

DB_PATH = './comments.db'   # Update this path accordingly


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