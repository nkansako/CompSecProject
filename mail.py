from pyOutlook import OutlookAccount
from msal import PublicClientApplication
import database

config = open('config.txt','r')
appid = config.readline().strip()
auth = config.readline().strip()
config.close()

app = PublicClientApplication(
    appid,
    authority=auth)

result = None
accounts = app.get_accounts()
if accounts:
    print("accounts found:")
    for a in accounts:
        print(a["username"])

#lifted from https://github.com/AzureAD/microsoft-authentication-library-for-python
if not result:
    # So no suitable token exists in cache. Let's get a new one from AAD.
    result = app.acquire_token_interactive(  # It automatically provides PKCE protection
         scopes=["https://outlook.office.com/User.Read","https://outlook.office.com/Mail.Read","https://outlook.office.com/email","https://outlook.office.com/Mail.Read.Shared","https://outlook.office.com/Mail.ReadBasic"])
if "access_token" in result:
    print(result["access_token"])  # Yay!
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug
#end theft


token = result["access_token"]
account = OutlookAccount(token)


conn = database.create_connection()
cur = database.create_cursor(conn)
database.format_table(conn,cur)



#msg_head = account.get_messages(page=0)
#print(msg_head[0])

inbox = account.inbox()
print("inbox body:",inbox[0].body)
print("inbox json:",inbox[0].api_representation)
print("inbox attachment:",inbox[0].attachments)
print("inbox message_id:",inbox[0].message_id)

for i in range(20):
    body = inbox[i].body
    msgid = inbox[i].message_id
    database.db_insert(conn,cur,body,msgid)

get = database.db_get(conn,cur)
print(get[0][0])
database.db_close(conn)
import mailparser
import logging


def authenticate_and_get_messages():
    config = open('config.txt', 'r')
    appid = config.readline().strip()
    auth = config.readline().strip()
    config.close()
    logging.info("Authorizing email access")
    app = PublicClientApplication(
        appid,
        authority=auth)

    result = None
    accounts = app.get_accounts()
    if accounts:
        print("accounts found:")
        logging.info("Accounts found")
        for a in accounts:
            print(a["username"])

    # lifted from https://github.com/AzureAD/microsoft-authentication-library-for-python
    if not result:
        # So no suitable token exists in cache. Let's get a new one from AAD.
        result = app.acquire_token_interactive(  # It automatically provides PKCE protection
             scopes=["https://outlook.office.com/User.Read", "https://outlook.office.com/Mail.Read","https://outlook.office.com/email","https://outlook.office.com/Mail.Read.Shared","https://outlook.office.com/Mail.ReadBasic"])
    if "access_token" in result:
        print(result["access_token"])  # Yay!
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug
    # end theft

    token = result["access_token"]
    account = OutlookAccount(token)

    # msg_head = account.get_messages(page=0)
    # print(msg_head[0])
    logging.info("Collecting inbox")
    inbox = account.inbox()
    logging.info("Inbox found")
    # print("inbox body:", inbox[0].body)

    return inbox
    #mailparser.parse_all_emails(inbox)
