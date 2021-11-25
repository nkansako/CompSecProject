import json
import requests
from os.path import exists

urlList = []
isPhish = False

if not exists("PhishTank.json"):
    print("Database not found, downloading...")

    url = requests.get("http://data.phishtank.com/data/online-valid.json")
    list = json.loads(url.text)

    for line in list:
        for key, value in line.items():
            if key == "url":
                urlList.append("{}".format(value))

    with open("PhishTank.json", 'w') as f:
        json.dump(urlList, f)

    print("Database downloaded!")
else:
    print("Database found!")
    with open("PhishTank.json", 'r') as f:
        urlList = json.load(f)


for i in urlList:
    if i == "URLHERE":
        isPhish = True

return isPhish




