from flask import render_template, request
import requests
from app.main import main
import json
import ast
from ..db.db_controller import get_userId_by_email


@main.route("/", methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route("/api/v1/jira/login", methods=['POST'])
def jira_login():
    username = request.form['username']
    password = request.form['password']
    body = {"username": 'jj51', "password": 'newegg@123'}
    headers = {'Content-Type': 'application/json'}
    address = 'http://jira/rest/auth/1/session'
    response = requests.post(address, headers=headers, data=json.dumps(body))
    cookies = ''.join(
        ['JSESSIONID=', response.cookies['JSESSIONID'], ';atlassian.xsrf.token=',
         response.cookies['atlassian.xsrf.token']])
    print cookies
    login_info(cookies)
    userInfo = user_info(username, cookies)
    user_email = json.loads(userInfo)['emailAddress']
    print user_email
    print get_userId_by_email(user_email)


def login_info(cookie):
    address = "http://jira/rest/auth/1/session"
    headers = {'Cookie': cookie}
    response = requests.get(address, headers=headers)
    return response.content


def user_info(username, cookie):
    address = ''.join(["http://jira/rest/api/2/user?username=", username])
    headers = {'Cookie': cookie}
    response = requests.get(address, headers=headers)
    print response.content
    return response.content

    # @main.route('api/v1/report/user/<userId>/<data>/<dayNum>')
    # def report():
