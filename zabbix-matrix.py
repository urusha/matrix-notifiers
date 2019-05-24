#!/usr/bin/python3

URL   = "https://localhost:8448"
TOKEN = "access_token"

###############################

import sys
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from markdown import markdown

roomid = sys.argv[1]
subject = sys.argv[2]
message = sys.argv[3]

########################################

html = markdown(message,extensions=['markdown.extensions.nl2br'])
text = ''.join(BeautifulSoup(html,"lxml").findAll(text=True))

# add subject
text = subject+'\n'+text
html = '<b>'+subject+'</b>'+html

# plain
#payload = { "msgtype": "m.text", "body": message }
# markdown
payload = { "msgtype": "m.text",  "body": text, "formatted_body": html, "format": "org.matrix.custom.html" }

headers = { 'Authorization': 'Bearer '+TOKEN }

url = URL+"/_matrix/client/r0/rooms/"+quote_plus(roomid)+"/send/m.room.message"

r = requests.post(url,json=payload,headers=headers,timeout=30)
if r.status_code != 200:
    print(r.status_code)
    print(r.text)
    exit(1)
