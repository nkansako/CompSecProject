
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
import tkinter as tk

nltk.download('stopwords')
import numpy as np


def write(*message, end="\n\n", sep=" "):
    text = ""
    for item in message:
        text += "{}".format(item)
        text += sep
    text += end
    console.insert(tk.INSERT, text)
    console.see("end")
    window.update()


def main():
    # TODO write main functionality

    # init_logger()
    messages = mail.getMail(account)
    write("Got ", len(messages), " messages.")

    logging.info("Parsing emails")

    add_messages_to_database(messages)

    check_emails()


def collect_mails():
    messages = mail.getMail(account)
    write("Got ", len(messages), " messages.")

    logging.info("Parsing emails")

    add_messages_to_database(messages)


def add_messages_to_database(messages):
    parsed = mailparser.parse_all_emails(messages)
    logging.info("Emails parsed")
    for email in parsed:
        # email["text"] = nlp.remove_stop_words(email["text"]) can use to remove extra stuff if needed
        text = email["text"]
        ex_score = nlp.score_exclamation_marks(text)
        textwosw = nlp.remove_stop_words(text, 3)
        keywords = nlp.find_keywords(textwosw)
        # print()("Text without editing:", text)
        # print()("Text with stopwords removed:", textwosw)
        # print()("keywords from nlp:", keywords)
        body = text
        body = body.replace(u'\xa0', u' ')
        msgid = email["m_id"]
        sender = email["email"]
        links = email["links"]
        print("links in addmsgtodb:",links)
        j = []
        for i in range(len(links)):
            if 'mailto' in links[i]:
                j.append(i)
        for i in range(len(j)):
            x = j.pop()
            print("deleting false link before db insert:",links[x])
            del links[x]
            np.subtract(j,1)
        attachments = email["attachment_names"]
        database.db_insert(conn, cur, body, msgid, sender, links, ex_score, attachments, keywords)


def check_emails():
    try:
        get = database.db_get(conn, cur)
        if len(get) == 0:
            return 0
        write("\n......................................................................................................................................................")
        for i in range(config.email_count):
            score = 1
            parsedGet = database.parseGet(get[i])
            if parsedGet["checked"] == 0:
                sender_val = nlp.check_domain(parsedGet["sender"])
                if sender_val:
                    write(
                        "This email came from a university staff member or another student\nWhile this makes the email more likely to not be malicious, do not rely on only this information, the email could also be stolen!")
                    write("Sender: ", parsedGet["sender"])
                else:
                    write(
                        "This email came from outside of the university!\nWhile this does not make the sender malicious, remain cautious!")
                    write("Sender: ", parsedGet["sender"])
                    if (score > 0.5):
                        score = 0.5
                for link in parsedGet["links"]:
                    url_value = phishcheck.checkurl(link)
                    if url_value > 0.8:
                        write("Link: ", link, " is fishy ")
                        if (score > 0):
                            score = 0
                    else:
                        write("Link: ", link, " does not seem to be fishy")
                    url_value2 = nlp.check_link(link)
                    if url_value2:
                        write("This link: ", link, " should be from university website")
                    else:
                        write("This link: ", link, " should be from outside of the university website")
                        if (score > 0.5):
                            score = 0.5
                if parsedGet["attachments"] != 0:
                    for attachment in parsedGet["attachments"]:
                        write(attachment)
                        attachment_val = nlp.dummy_check_attachment(attachment)
                        if attachment_val == 1.0:
                            write("Nothing fishy here in attachment: ", attachment, " file type should be safe")
                        elif attachment_val == 0.5:
                            write("Something may be fishy about attachment: ", attachment,
                                  " file type is often used maliciously")
                        if (not url_value2 and score > 0.5):
                            score = 0.5
                        else:
                            write("This file is very suspicious, do not open the file! Attachment: ", attachment)
                            if (score > 0):
                                score = 0

                #if checked.get():
                #    links = crawl(parsedGet["keywords"])
                #    print_crawled_links(links)
                database.db_update_score(conn, cur, parsedGet["msg_id"], score)
                database.db_update_status(conn, cur, parsedGet["msg_id"])

                write("......................................................................................................................................................")
    except AttributeError as e:
        print(e)
        write("No collected emails, collect emails first!")


                # if nlp.check_sender_name(parsedGet["sender"]):

                #  print()("Crawling for keywords:", parsedGet["keywords"], "...")
                #  tmp = webcrawler.crawl(parsedGet["keywords"])
                #  print()("Crawled and got return:", tmp)


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
            print(
                "This email came from outside of the university!\nWhile this does not make the sender malicious, remain cautious!")
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


def print_checked_mails():
    global conn, cur
    get = database.db_get(conn, cur)
    for i in range(len(get)):
        if (get[i][7] == 1):
            print("Message:", get[1], ". Score:", get[4])


def crawl() -> list:
    try:
        get = database.db_get(conn, cur)
        write("\n......................................................................................................................................................")
        links = []
        for i in range(config.email_count):
            parsedGet = database.parseGet(get[i])
            if parsedGet["checked"] == 0:
                keywords = parsedGet["keywords"]
                if keywords != 0:
                    val = webcrawler.crawl(keywords)
                    links = []
                    for _ in val:
                        links.append(_[0])
            write("\n......................................................................................................................................................")
        return links
    except AttributeError as e:
        print("No collected emails, collect emails first")


def print_crawled_links(links: list):
    write("Crawled university website for links and found following news items: ")
    for link in links:
        write(link)


def gui_login():
    global account
    # run_tests()
    # authenticate, get account token
    account = mail.authenticate()
    if account != "":
        write("Login succesfully")
        login_button.pack_forget()
        collect_button.pack(side=tk.LEFT)
        check_button.pack(side=tk.LEFT)
        #crawl_check.pack(side=tk.LEFT)
        crawl_button.pack(side=tk.LEFT)
        score_button.pack(side=tk.LEFT)


    else:
        write("Login failed, try again")


def gui_checkmail():
    # call main()
    #main()
    check_emails()
    write("Done checking emails")


def gui_score():
    print("Score button pressed.")
    # global conn,cur
    get = database.db_get(conn, cur)
    print("Got a get in gui_score of len:", len(get))
    for i in range(len(get)):
        print("get7 value:", get[i][7])
        if (get[i][7] == 1):
            print("Found a checked mail.")
            tmp = 0
            prevspace = 0
            write("Body:\"", end="")
            for k in get[i][0]:
                if (k == "\n" and prevspace == 0):
                    k = " "
                    prevspace = 1
                elif ((k == "\n" or k == " ") and prevspace == 1):
                    k = ""
                elif (k == " "):
                    prevspace = 1
                else:
                    prevspace = 0
                write(k, end="")
                tmp += 1
                if (tmp > 50):
                    break
            write("\"...\nMessage ID:", get[i][1], ". Score:", get[i][4], end="")
            if (get[i][4] == '1'):
                write(", likely safe.")
            elif (get[i][4] == '0.5'):
                write(", care required, likely contains odd attachments/links to outside the university.")
            elif (get[i][4] == '0'):
                write(", suspicious.")


def gui_crawl():
    write("Crawling....")
    links_ = crawl()
    print_crawled_links(links_)
    for link in links_:
        print(link)
    write("Done crawling emails")


def gui_quit():
    window.destroy()


def gui_collect():
    global conn, cur
    write("Checking mails, please wait...")
    write("Creating database...")
    conn = database.create_connection()
    cur = database.create_cursor(conn)
    database.format_table(conn, cur)
    collect_mails()
    write("Done collecting mails")

# GUI
if __name__ == '__main__':
    account = ""
    conn = ""
    cur = ""

    window = tk.Tk()
    window.title('CompSec email checker')
    window.resizable(0, 0)

    login_button = tk.Button(window, text="Login ", command=gui_login)
    check_button = tk.Button(window, text="Check Mails", command=gui_checkmail)
    score_button = tk.Button(window, text="Score", command=gui_score)
    crawl_button = tk.Button(window, text="Crawl university website", command=gui_crawl)
    collect_button = tk.Button(window, text="Collect emails", command=gui_collect)
    quit_button = tk.Button(window, text="Quit", command=gui_quit)

    #checked = tk.BooleanVar()
    #crawl_check = tk.Checkbutton(window, text="Crawl links while checking emails", variable=checked, onvalue=True, offvalue=False)

    console = tk.Text(window, height=25, width=150)

    console.pack(side=tk.TOP)
    login_button.pack(side=tk.LEFT)
    quit_button.pack(side=tk.RIGHT)

    startTime = time.perf_counter()
    window.mainloop()

    # close DB
    if conn != "":
        database.db_close(conn)
