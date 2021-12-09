import json
import os.path
import time
from difflib import SequenceMatcher

import requests
from os.path import exists


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def checkurl(url: str) -> float:
    url_list = []
    is_phish = 0

    if not exists("PhishTank.json") or (time.time() - os.path.getmtime("PhishTank.json")) >= (7 * 24 * 60 * 60):
        print("Database not found or it's need update, downloading...")

        # full_list = json.loads(requests.get("https://data.phishtank.com/data/online-valid.json").text)
        full_list = json.load(open("verified_online.json"))
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
        similarity = similar(i, url)
        if similarity >= 0.8:  # Matching percentage, 80% as default.
            if similarity > is_phish:
                is_phish = similarity

    return is_phish  # Returns highest similarity percentage
