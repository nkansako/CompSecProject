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
import webcrawler
import tester
import phishcheck
nltk.download('stopwords')

def main():
    # TODO write main functionality

    #init_logger()
    messages = mail.getMail(account)
    print("Got ",len(messages)," messages.")

    logging.info("Parsing emails")

    add_messages_to_database(messages)

    check_emails()


def add_messages_to_database(messages):
    parsed = mailparser.parse_all_emails(messages)
    logging.info("Emails parsed")
    for email in parsed:
        # email["text"] = nlp.remove_stop_words(email["text"]) can use to remove extra stuff if needed
        text = email["text"]
        ex_score = nlp.score_exclamation_marks(text)
        textwosw = nlp.remove_stop_words(text, 3)
        keywords = nlp.find_keywords(textwosw)
        #print("Text without editing:", text)
        #print("Text with stopwords removed:", textwosw)
        #print("keywords from nlp:", keywords)
        body = text
        body = body.replace(u'\xa0', u' ')
        msgid = email["m_id"]
        sender = email["email"]
        links = email["links"]
        attachments = email["attachment_names"]
        database.db_insert(conn, cur, body, msgid, sender, links, ex_score, attachments, keywords)


def check_emails():
    get = database.db_get(conn, cur)
    for i in range(len(get)):
        parsedGet = database.parseGet(get[i])
        if parsedGet["checked"] == 0:
            sender_val = nlp.check_domain(parsedGet["sender"])
            if sender_val:
                print("This email came from a university staff member or another student\nWhile this makes the email more likely to not be malicious, do not rely on only this information, the email could also be stolen!")
                print("Sender: ", parsedGet["sender"])
            else:
                print("This email came from outside of the university!\nWhile this does not make the sender malicious, remain cautious!")
                print("Sender: ", parsedGet["sender"])
            for link in parsedGet["links"]:
                url_value = phishcheck.checkurl(link)
                if url_value > 0.8:
                    print("Link: ", link, " is fishy ")
                else:
                    print("Link: ", link, " does not seem to be fishy")
                url_value2 = nlp.check_link(link)
                if url_value2:
                    print("This link: ", link, " should be from university website")
                else:
                    print("This link: ", link, " should be from outside of the university website")
            if parsedGet["attachments"] != 0:
                for attachment in parsedGet["attachments"]:
                    print(attachment)
                    attachment_val = nlp.dummy_check_attachment(attachment)
                    if attachment_val == 1.0:
                        print("Nothing fishy here in attachment: ", attachment, " file type should be safe")
                    elif attachment_val == 0.5:
                        print("Something may be fishy about attachment: ", attachment,
                              " file type is often used maliciously")
                    else:
                        print("This file is very suspicious, do not open the file! Attachment: ", attachment)
            #if nlp.check_sender_name(parsedGet["sender"]):

              #  print("Crawling for keywords:", parsedGet["keywords"], "...")
              #  tmp = webcrawler.crawl(parsedGet["keywords"])
              #  print("Crawled and got return:", tmp)



def init_logger():
    file = config.input_f + config.logger_name
    logging.basicConfig(filename=file, level=logging.DEBUG)


def run_tests():
    print("Creating database for test set")
    conn1 = database.create_connection()
    cur = database.create_cursor(conn1)
    database.format_table(conn1, cur)
    print("Database created successfully")
    senders, subjects, bodies, links, ids, attachments = tester.create_test_cases()
    for i in range(len(ids)):
        ex_score = nlp.score_exclamation_marks(bodies[i])
        keywords = nlp.find_keywords(nlp.remove_stop_words(bodies[i], 1))
        database.db_insert(conn1, cur, bodies[i], ids[i], senders[i], links[i], ex_score, attachments[i], keywords)
    get = database.db_get(conn1, cur)
    for i in range(len(get)):

        parsedGet = database.parseGet(get[i])
        print("Message id ", parsedGet["msg_id"])
        if int(parsedGet["msg_id"]) > 5:
            print("This should be seen as malicious!")
        else:
            print("This should be seen as ok or suspicious!")
        sender_val = nlp.check_domain(parsedGet["sender"])
        if sender_val:
            print(
                "This email came from a university staff member or another student\nWhile this makes the email more likely to not be malicious, do not rely on only this information, the email could also be stolen!")
        else:
            print("This email came from outside of the university!\nWhile this does not make the sender malicious, remain cautious!")
        for link in parsedGet["links"]:
            print("LINKKEJÄ!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            url_value = phishcheck.check_url(link)
            if url_value > 0.8:
                print("Link: ", link, " is fishy ")
            url_value2 = nlp.check_link(link)
            if url_value2:
                print("This link: ", link, " should be from university website")
            else:
                print("This link: ", link, " should be from outside of the university website")

        for attachment in parsedGet["attachments"]:
            attachment_val = nlp.dummy_check_attachments(attachment)
            if attachment_val == 1.0:
                print("Nothing fishy here in attachment: ", attachment, " file type should be safe")
            elif attachment_val == 0.5:
                print("Something may be fishy about attachment: ", attachment, " file type is often used maliciously")
            else:
                print("This file is very suspicious, do not open the file! Attachment: ", attachment)

    database.db_close(conn1)


if __name__ == "__main__":
    #run_tests()
    startTime = time.perf_counter()
    #authenticate, get account token
    account = mail.authenticate()
    #format database
    print("Creating database...")
    conn = database.create_connection()
    cur = database.create_cursor(conn)
    database.format_table(conn,cur)
    #call main()
    main()
    #close DB
    database.db_close(conn)
