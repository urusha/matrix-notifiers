#!/usr/bin/env python3

URL = "https://localhost:8448"
TOKEN  = "your_matrix_token"
BIND = "127.0.0.1"
PORT = 3001
AUTH = "your_sercret_string"

# INSTALL:
# apt:
# apt-get install python3 python3-requests python3-urllib3 python3-markdown python3-bs4
# or pip:
# pip3 install requests urllib3 Markdown beautifulsoup4

##############################################

from http.server import BaseHTTPRequestHandler, HTTPServer
import socketserver
import json
import re
from datetime import datetime

# matrix
import sys
import requests
from bs4 import BeautifulSoup
from markdown import markdown
from urllib.parse import quote_plus
import time

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(str('{"status":"ERROR","text":"GET not supported"}\n').encode('utf-8'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_json=json.loads(post_data.decode('utf-8'))

        path = self.path[1:].split('/')

        if path[0] != AUTH:
            self.send_response(403)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes('{"status":"ERROR","text":"Unauthorized"}\n', 'utf-8'))

        roomid = path[1]

        headers = { 'Authorization': 'Bearer '+TOKEN }
        url = URL+"/_matrix/client/r0/rooms/"+quote_plus(roomid)+"/send/m.room.message"

        # make call before message
        if post_json['state']=="alerting" and len(path)>2 and path[2]=="call":
            call_id = "grafana"
            lifetime = 10
            payload1 = { "call_id": call_id, "lifetime": lifetime*1000, "offer": { "sdp": "", "type": "offer" }, "version": "0" }
            payload2 = { "call_id": call_id, "version": "0" }
            url1 = URL+"/_matrix/client/r0/rooms/"+quote_plus(roomid)+"/send/m.call.invite"
            url2 = URL+"/_matrix/client/r0/rooms/"+quote_plus(roomid)+"/send/m.call.hangup"
            r1 = requests.post(url1,json=payload1,headers=headers,timeout=30)
            # workaround  https://github.com/vector-im/riot-android/issues/2741
            time.sleep(lifetime)
            r2 = requests.post(url2,json=payload2,headers=headers,timeout=30)

        subject = post_json['state'].upper() + ': '+ post_json['ruleName']
        if 'message' in post_json:
            message = post_json['message'] + '\n'
        else:
            message = ''
        for i in post_json['evalMatches']:
            message = message + str(i['metric']) + ': ' + str(i['value']) + '\n'

        html = markdown(message,extensions=['markdown.extensions.nl2br'])
        text = ''.join(BeautifulSoup(html,"lxml").findAll(text=True))
        # add subject
        text = subject+'\n'+text
        html = '<b>'+subject+'</b>'+html

        payload = { "msgtype": "m.text",  "body": text, "formatted_body": html, "format": "org.matrix.custom.html" }

        r = requests.post(url,json=payload,headers=headers,timeout=30)
        if r.status_code != 200:
            status = 'ERROR'
            text = r.text
        else:
            status = 'OK'
            text = ''

        self.send_response(r.status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(bytes('{"status": "%s","text":"%s"}' % (status, text), 'utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=3001):
    server_address = (BIND, PORT)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
