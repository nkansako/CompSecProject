from bs4 import BeautifulSoup
import re


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


def parse_all_emails(email_list: list) -> list:
    parsedMails = []
    for email in email_list:
        m_id, sender_email, subject, text, links, hyperlinks = mailparser(email)
        all_links = links + hyperlinks
        parsed = {"m_id": m_id, "email": sender_email, "subject": subject, "text": text, "links": all_links}
        parsedMails.append(parsed)
    return parsedMails
