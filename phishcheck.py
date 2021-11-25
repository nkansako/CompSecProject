import json
import requests
from os.path import exists


def checkurl(url: str) -> bool:
    url_list = []
    is_phish = False

    if not exists("PhishTank.json"):
        print("Database not found, downloading...")

        url = requests.get("http://data.phishtank.com/data/online-valid.json")
        full_list = json.loads(url.text)

        for line in full_list:
            for key, value in line.items():
                if key == "url":
                    url_list.append("{}".format(value))

        with open("PhishTank.json", 'w') as f:
            json.dump(url_list, f)

        print("Database downloaded!")
    else:
        print("Database found!")
        with open("PhishTank.json", 'r') as f:
            url_list = json.load(f)

    for i in url_list:
        if i == url:
            is_phish = True

    return is_phish
