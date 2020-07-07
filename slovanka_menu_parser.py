#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime,timedelta

resp = requests.get('http://www.jidelnaslovanka.cz/english-menu/')
txt = resp.text
#print(txt)
soup = BeautifulSoup(txt, 'lxml')

text = ""

for row in soup.find_all('div',attrs={"class" : "et_pb_text_inner"}):
    text = text + row.text + "\n"


dow = datetime.today().strftime('%-d.%-m. %A')

tomorrow_dt = datetime.today() + timedelta(days=1)
tomorrow = tomorrow_dt.strftime('%-d.%-m. %A')


dayfound = False

daymenu = ""

for line in text.split('\n'):
    if "{}".format(dow) in line:
        dayfound = True
    if "{}".format(tomorrow) in line:
        break

    if dayfound and line.strip() != "":
        daymenu = daymenu + line + '\n'

## the Slack part

import logging
#logging.basicConfig(level=logging.DEBUG)

import os
from slack import WebClient
from slack.errors import SlackApiError

#slack_token = os.environ["SLACK_API_TOKEN"]
slack_token = "ULTRA_SECRET"
client = WebClient(token=slack_token)

try:
  response = client.chat_postMessage(
    channel="SECRET_a_bit_too",
    text=daymenu
    #text=":tada:"
  )
except SlackApiError as e:
  # You will get a SlackApiError if "ok" is False
  assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
