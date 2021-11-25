import sqlite3
from sqlite3 import Error

#create a database connection to a SQLite database
def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(':memory:') #create db in memory rather than file
        print("db connection succesful with sqlite: ",sqlite3.version)
        return conn
    except Error as e:
        print(e)

#create cursor to execute commands
def create_cursor(conn):
    cur = conn.cursor()
    return cur

def db_close(conn):
    conn.close
    print("Database succesfully closed.")

def format_table(conn,cur):
    cur.execute("DROP TABLE IF EXISTS MAIL")
    com = 'CREATE TABLE MAIL(BODY CHAR(12345), MSG_ID CHAR(1024))'
    cur.execute(com)
    print("DB: table 'mail' created successfully")
    conn.commit

#insert checks if message already exists.
def db_insert(conn,cur,body,msg_id):
    try:
        (body, msg_id) = (body),(msg_id)
        cur.execute('SELECT msg_id FROM mail WHERE msg_id = ?',(msg_id,))
        get = cur.fetchall()
        if len(get)!=0:
            print("message already exists in database.")
        else:
            cur.execute('INSERT INTO MAIL(BODY, MSG_ID) VALUES (?, ?)',(body,msg_id))
            conn.commit()
            print("message succesfully saved to database.")
    except Error as e:
        print(e)

def db_get(conn,cur):
    try:
        #(string1, string2) = (string1),(string2)
        cur.execute('SELECT * FROM MAIL')
        get = cur.fetchall()
        conn.commit()
        print("table succesfully read")
        return get
    except Error as e:
        print(e)