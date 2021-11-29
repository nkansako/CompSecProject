import sqlite3
from sqlite3 import Error
import ast

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
    com = 'CREATE TABLE MAIL(BODY CHAR(12345) NOT NULL, MSG_ID CHAR(1024) NOT NULL, SENDER CHAR(255) NOT NULL, LINKS CHAR(12345) NOT NULL, SCORE CHAR(255) NOT NULL, ATTACHMENTS CHAR(1024) NOT NULL)'
    cur.execute(com)
    print("DB: table 'mail' created successfully")
    conn.commit

#insert checks if message already exists.
def db_insert(conn,cur,body,msg_id,sender,links,score,attachments):
    try:
        if(len(attachments)==0):
            attachments = 0
        (body, msg_id, sender, links, score, attachments) = (str(body)),(str(msg_id)),(str(sender)),(str(links)),(str(score)),(str(attachments))
        cur.execute('SELECT msg_id FROM mail WHERE msg_id = ?',(msg_id,))
        get = cur.fetchall()
        if len(get)!=0:
            print("message already exists in database.")
        else:
            cur.execute('INSERT INTO MAIL(BODY, MSG_ID, SENDER, LINKS, SCORE, ATTACHMENTS) VALUES (?, ?, ?, ?, ?, ?)',(body,msg_id,sender,links,score,attachments))
            conn.commit()
            print("message succesfully saved to database.")
    except Error as e:
        print("ERROR in db_insert: ",e)

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

def parseGet(get):
    try:
        tmp = ast.literal_eval(get[3])
        parsedGet = {"body": get[0], "msg_id": get[1], "sender": get[2], "links": tmp, "score": get[4], "attachments": get[5]}
        return parsedGet
    except Error as e:
        print("error in getToList: ",e)