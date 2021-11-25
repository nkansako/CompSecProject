from bs4 import BeautifulSoup
import re


class parsedMail:

    parsed = {
        "m_id": "",
        "email": "",
        "subject": "",
        "text": "",
        "all_links": []
    }

    def __init__(self, message_id: str, sender_email: str, subject_text: str, text_body: str, all_links: list):
        self.parsed["m_id"] = message_id
        self.parsed["email"] = sender_email
        self.parsed["subject"] = subject_text
        self.parsed["text"] = text_body
        self.parsed["all_links"] = all_links


def extract_links(text: str) -> list:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, text)
    return [x[0] for x in url]


def mailparser(email):
    # TODO: fix sender email and name
    body = email.body
    sender = email.sender
    sender_email = sender.email
    subject = email.subject
    m_id = email.message_id

    soup = BeautifulSoup(body, features="html.parser")

    text = soup.get_text()
    hyperlinks = []
    for link in soup.findAll("a"):
        hyperlinks.append(link.get("href"))

    links = extract_links(text)
    return m_id, sender_email, subject, text, links, hyperlinks


def parse_all_emails(email_list: list) -> dict:
    parsedMails = []
    for email in email_list:
        m_id, sender_email, subject, text, links, hyperlinks = mailparser(email)
        all_links = links + hyperlinks
        mail = parsedMail(m_id, sender_email, subject, text, all_links)
        parsedMails.append(mail)
    return parsedMails
