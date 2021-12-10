# CompSecProject
Computer security project 2021


This repository contains the code for the University Email Checker tool made for Computer security project 2021.

To run the code, you need to have the dependencies explained in the requirements.txt file and a a working appid and auth address for the Outlook API. These should be included in a file called config.txt

With these requirements met, the code can be ran from the command line 

```
python main.py
```

This will open the GUI

Pressing log in will open a browser tab that asks you to log in to your Outlook account. In case you are already logged in, you only need to authorize this application (first time only)

After logging in, the program has access to your Outlook email inbox. It will only read *your* emails, and will not send anything, or collect any information for further use. Everything is stored locally in a memory based database, so that anything will be erased after shutting down the program.
