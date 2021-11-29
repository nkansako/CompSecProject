import mail
import mailparser
import nlp
import logging
import config
import database
import nltk
nltk.download('punkt')
import ast
import time


def main():
    # TODO write main functionality

    #init_logger()
    messages = mail.getMail(account)
    print("Got ",len(messages)," messages.")
    #for i in range(len(messages) or 20):
    #    body = messages[i].body
    #    msgid = messages[i].message_id
    #    database.db_insert(conn,cur,body,msgid)
    #get = database.db_get(conn,cur)
    #print("DB GET succesful!")


    logging.info("Parsing emails")
    parsed = mailparser.parse_all_emails(messages)
    logging.info("Emails parsed")
    for email in parsed:
        # email["text"] = nlp.remove_stop_words(email["text"]) can use to remove extra stuff if needed
        text = email["text"]
        ex_score = nlp.score_exclamation_marks(text)
        keywords = nlp.find_keywords(text)
        web_crawler(keywords)
        body = text
        msgid = email["m_id"]
        sender = email["email"]
        links = email["links"]
        attachments = email["attachment_names"]
        
        database.db_insert(conn,cur,body,msgid,sender,links,ex_score,attachments)
    get = database.db_get(conn,cur)
    parsedGet = database.parseGet(get[0])
    print(parsedGet["links"])



def check_file():
    # TODO write something that checks a file if malicious
    pass


def check_url():
    # TODO write something that checks url if phishing site etc
    pass


def find_keywords():
    # TODO write something that finds most common words in the body of the email
    pass


def web_crawler(keywords: list) -> list:
    # TODO write something that crawls university website for possible matches in email
    return []


def init_logger():
    file = config.input_f + config.logger_name
    logging.basicConfig(filename=file, level=logging.DEBUG)


if __name__ == "__main__":
    startTime = time.perf_counter()
    #authenticate, get account token
    account = mail.authenticate()
    #format database
    print("Creating database...")
    conn = database.create_connection()
    cur = database.create_cursor(conn)
    database.format_table(conn,cur)
    main()
    #close DB
    database.db_close(conn)