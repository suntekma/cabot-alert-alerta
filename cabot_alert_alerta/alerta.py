#!/usr/bin/env python
# coding:utf-8
import sys
import urllib2
import time
import json
import requests
from os import environ as env
# reload(sys)
# sys.setdefaultencoding('utf-8')

alertaURL = env.get('AlertaURL','http://alerta.newegg.org:8080/api/alert')
key = env.get('key','vx_DVeHIy2ZbslaHf13GYHHW1Kj2zJpJEkPLcQnd')
headers = {
    'Content-Type': "application/json",
    'Authorization': "Key " + key ,
    }

def send_msg(playload):
    # 发送消息
    payload = playload

    response = requests.request("POST", url=alertaURL, data=payload, headers=headers)

    print(response.text)
