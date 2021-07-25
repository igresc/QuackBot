import requests


url = "https://discord.com/api/v8/applications/516220021534490652/commands"

json = {
    "name": "ping",
    "description": "Ping QuackBot",
    "options": []
}

# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot NTE2MjIwMDIxNTM0NDkwNjUy.W_qNXA.VSqGN0G1ZAj-fNMAMBvWxSWfAqw"
}

# or a client credentials token for your app with the applications.commands.update scope
# headers = {
#     "Authorization": "Bearer <my_credentials_token>"
# }

r = requests.post(url, headers=headers, json=json)
print(r.text)