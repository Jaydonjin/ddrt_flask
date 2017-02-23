from flask import request
import json
import requests


def jira_login(body):
    address = 'http://jira/rest/auth/1/session'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(address, headers=headers, data=json.dumps(body))
    return response


def jire_logout(headers):
    address = 'http://jira/rest/auth/1/session'
    response = requests.delete(address, headers=headers)
    return response


def jira_serach(cookies):
    playload = request.get_json(True)
    address = "http://jira/rest/api/2/search"
    headers = {"content-type": "application/json", "Cookie": cookies}
    response = requests.post(address, headers=headers, json=playload)
    return response
