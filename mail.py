from pyOutlook import OutlookAccount
from msal import PublicClientApplication

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

#msg_head = account.get_messages(page=0)
#print(msg_head[0])

inbox = account.inbox()
print("inbox body:",inbox[0].body)