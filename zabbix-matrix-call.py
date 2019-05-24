#!/usr/bin/python3

URL   = "https://localhost:8448"
TOKEN = "access_token"

###############################

import sys
import requests
from urllib.parse import quote_plus

call_id = "zabbix"
roomid = sys.argv[1]
subject = sys.argv[2]
#message = sys.argv[3]
if subject.startswith('OK'):
    exit(0)
#lifetime = sys.argv[2]
#lifetime = int(lifetime)
lifetime = 10

headers = { 'Authorization': 'Bearer '+TOKEN }

payload = { "call_id": call_id, "lifetime": lifetime*1000, "offer": { "sdp": "", "type": "offer" }, "version": "0" }
payload2 = { "call_id": call_id, "version": "0" }

url  = URL+"/_matrix/client/r0/rooms/"+quote_plus(roomid)+"/send/m.call.invite"
url2 = URL+"/_matrix/client/r0/rooms/"+quote_plus(roomid)+"/send/m.call.hangup"

r = requests.post(url,json=payload,headers=headers,timeout=30)
if r.status_code != 200:
    print(r.status_code)
    print(r.text)
    exit(1)

# workaround  https://github.com/vector-im/riot-android/issues/2741
import time
time.sleep(lifetime)

r2 = requests.post(url2,json=payload2,headers=headers,timeout=30)
if r2.status_code != 200:
    print(r2.status_code)
    print(r2.text)
    exit(1)
