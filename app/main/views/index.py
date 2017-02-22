from flask import render_template, request
import requests
from app.main import main
import json
import datetime
from ..db.db_controller import *

cur_cookie = None
username = None


@main.route("/", methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route("/api/v1/jira/login", methods=['POST', 'DELETE'])
def jira_login():
    address = 'http://jira/rest/auth/1/session'
    print request.method
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']
        body = {"username": username, "password": password}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(address, headers=headers, data=json.dumps(body))
        cookies = ''.join(
            ['JSESSIONID=', response.cookies['JSESSIONID'], ';atlassian.xsrf.token=',
             response.cookies['atlassian.xsrf.token']])
        global cur_cookie
        cur_cookie = cookies
        # login_info(cookies)
        user = user_info(username, cookies)
        user = json.loads(user)
        user_email = user['emailAddress']
        user_id = get_user_id_by_email(user_email)
        group_id = get_group_id_by_user_id(user_id)
        domain_id = get_domain_id_by_user_id(user_id)
        group_name = get_group_name_by_id(group_id)
        domain_name = get_domain_name_by_id(domain_id)
        user['userId'] = user_id
        user['groupName'] = group_name
        user['domainName'] = domain_name
        user = json.dumps(user)
        return user, 200

    else:
        headers = {'Cookie': cur_cookie}
        print headers
        response = requests.delete(address, headers=headers)
        return response.content, response.status_code


@main.route("/api/v1/jira/user")
def login_again():
    user = user_info(username, cur_cookie)
    user = json.loads(user)
    user_email = user['emailAddress']
    user_id = get_user_id_by_email(user_email)
    group_id = get_group_id_by_user_id(user_id)
    domain_id = get_domain_id_by_user_id(user_id)
    group_name = get_group_name_by_id(group_id)
    domain_name = get_domain_name_by_id(domain_id)
    user['userId'] = user_id
    user['groupName'] = group_name
    user['domainName'] = domain_name
    user = json.dumps(user)
    return user, 200


@main.route('/api/v1/report/user/<user_id>/<day_num>')
def report(user_id, day_num):
    return report_date(user_id, day_num)


@main.route('/api/v1/issue/prev/<user_id>')
def history_issues(user_id):
    issue = get_history_issues_by_user_id(user_id)
    body = {'issue': issue, 'user_id': user_id}
    body = json.dumps(body)
    return body, 200


@main.route('/api/v1/jira/search', methods=['POST'])
def jira_search():
    test_body = {"jql": "key in ('DFIS-122') order by created, priority desc", "fields": ["id", "key", "summary"]}
    address = "http://jira/rest/api/2/search"
    headers = {"content-type": "application/json", "Cookie": cur_cookie}
    response = requests.post(address, headers=headers, data=json.dumps(test_body))
    return response.content, response.status_code


def login_info(cookie):
    address = "http://jira/rest/auth/1/session"
    headers = {'Cookie': cookie}
    response = requests.get(address, headers=headers)
    return response.content


def user_info(username, cookie):
    address = ''.join(["http://jira/rest/api/2/user?username=", username])
    headers = {'Cookie': cookie}
    response = requests.get(address, headers=headers)
    return response.content


def report_date(user_id, day_num):
    cur_report = get_report_by_user(user_id, day_num)
    body = [{'content': cur_report.content, 'date': cur_report.date.strftime("%Y-%m-%d %H:%M:%S"),
             'issue': cur_report.issue_name,
             'timeSpent': cur_report.time_spent, 'userid': cur_report.user_id, 'worklogId': cur_report.worklog_id}]
    body = json.dumps(body)
    return body, 200
