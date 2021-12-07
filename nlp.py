from nltk import FreqDist, word_tokenize
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from statistics import mean
import config


def remove_stop_words(line: str, repeat: int = 1) -> str:
    # We might not want to use this function at all, but it is here in case we need it
    # return line
    words = word_tokenize(line)
    sw = stopwords.words('english')
    for word in words:
        if (word.lower() in sw and word.lower()) or word.lower() in config.special_characters:
            words.remove(word)
    for i in range(len(words)):
        words[i] = words[i].lower()
    result = ' '.join(words)
    if repeat > 0:
        # due to complex word structure, the stop words removal will be ran multiple times
        result = remove_stop_words(result, repeat-1)
    return result


def find_keywords(text: str) -> list:
    tokens = word_tokenize(text)
    fd = FreqDist(tokens)
    keywords = fd.most_common(config.keyword_count)
    retval = []
    for key in keywords:
        retval.append(key[0])
    return retval


def check_domain(sender: str) -> bool:
    domain = sender.split("@")[1]
    if domain == config.domain_staff or domain == config.domain_student:
        return True
    else:
        return False


def check_sender_name(sender: str) -> bool:
    name = sender.split("@")[0]
    # TODO something that checks if name is fine
    if name == "paju-admin" or name == "ict-tiedote":
        return True
    else:
        return False


def score_exclamation_marks(text: str) -> float:
    count = text.count("!")
    if count <= 1:
        score = 1.0
    elif 1 < count < 5:
        score = 0.5
    else:
        score = 0.0
    return score


def sender_score(name: str, email: str) -> float:
    email_value = check_domain(email)
    name_value = check_sender_name(name)

    if email_value and name_value:
        score = 1.0
    elif not email_value and not name_value:
        score = 0.0
    else:
        score = 0.5
    return score


def cross_reference(text1: str, text2: str) -> float:

    similarities = []

    tokens1 = word_tokenize(remove_stop_words(text1))
    tokens2 = word_tokenize(remove_stop_words(text2))

    l1 = len(tokens1)
    l2 = len(tokens2)

    if l1 == l2:
        for i in range(l1):
            s = SequenceMatcher(None, tokens1[i], tokens2[i])
            similarity = s.ratio()
            similarities.append(similarity)
    elif l1 > l2:
        for i in range(l2):
            s = SequenceMatcher(None, tokens1[i], tokens2[i])
            similarity = s.ratio()
            similarities.append(similarity)
    else:
        for i in range(l1):
            s = SequenceMatcher(None, tokens1[i], tokens2[i])
            similarity = s.ratio()
            similarities.append(similarity)

    return mean(similarities)


def check_grammar(text: str) -> float:
    tokens = word_tokenize(text)
    for token in tokens:
        # TODO: something to check the grammar maybe
        pass


def dummy_check_attachment(attachment: str) -> float:
    c = attachment.count(".")
    print("c: ", c)
    if c > 0:
        extension = attachment.split(".")[1]
        if extension == "exe":
            return 0.0
        elif extension in config.possibly_dangerous:
            return 0.5
        else:
            return 1.0
    else:
        return 0.0


def check_link(link: str) -> bool:
    # Check if link is from university of Oulu
    if config.domain_staff in link and ".com" not in link and ".net" not in link:
        return True
    else:
        return False


#with open("testi.txt", "r") as file:
#    text = ""
#    for line in file.readlines():
#        text += line
#newText = remove_stop_words(text, 5)
#print(find_keywords(newText))