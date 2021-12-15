input_f = "input/"
output_f = "output/"

logger_name = "email_checker_log.txt"

check_files = True
check_urls = True
check_sender = True
check_body = True

keyword_count = 6
crawl_count = 3
email_count = 2  # max 10!

domain_staff = "oulu.fi"
domain_student = "student.oulu.fi"

special_characters = [",", ".", "/", "\"", ";", "-", "_", "!", "?", "(", ")", "--", ".\"", "!--", ",\"", ".--", "'", ":", "*", '""', '"', "``", "''", '’', '—', '‘', "»"]

search_beginning = "https://www.oulu.fi/fi/search?search_api_fulltext="
search_end = "&field_targeting=All"

crawl_base = "https://www.oulu.fi"

possibly_dangerous = ["pdf", "docx", "xlsx", "ppt", "doc", "xls", "jpeg", "pptx"]

dangerous = ["exe", "zip", "rar", "pif", "vbs", "scr", "rtf"]
