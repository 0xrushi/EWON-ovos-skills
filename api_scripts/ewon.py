#!/usr/bin/env python
# coding: utf-8

import requests
import urllib.parse

REMOTE_SERVER_IP = 'http://127.0.0.1:5000'

def send_emotion(st: str):
    url = REMOTE_SERVER_IP + '/parse_emotion'
    encoded_query = urllib.parse.quote(st)
    try:
        r = requests.get(f"{url}?query={encoded_query}")
        return r.json()['status']
    except:
        return "something wrong in the API server2"