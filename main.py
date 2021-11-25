import mail
import mailparser
import nlp
import logging
import config
import database
import nltk
nltk.download('punkt')


def main():
    # TODO write main functionality

    #init_logger()
    messages = mail.authenticate_and_get_messages()
    # add messages to DB
    print("Creating database...")
    conn = database.create_connection()
    cur = database.create_cursor(conn)
    database.format_table(conn,cur)
    print(len(messages))
    for i in range(len(messages) or 20):
        body = messages[i].body
        msgid = messages[i].message_id
        database.db_insert(conn,cur,body,msgid)
    get = database.db_get(conn,cur)
    print("DB GET succesful!")


    logging.info("Parsing emails")
    parsed = mailparser.parse_all_emails(messages)
    logging.info("Emails parsed")
    for email in parsed:
        # email["text"] = nlp.remove_stop_words(email["text"]) can use to remove extra stuff if needed
        text = email.parsed["text"]
        ex_score = nlp.score_exclamation_marks(text)
        keywords = nlp.find_keywords(text)
        web_crawler(keywords)

    #close DB
    database.db_close(conn)
    print("DB closed.")


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
    logging.basicConfig(filename=file, encoding='utf-8', level=logging.DEBUG)


if __name__ == "__main__":
    main()
