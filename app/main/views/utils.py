import requests
import json
from flask import request
from app.main.db.db_controller import *


def login_info(cookie):
    address = "http://jira/rest/auth/1/session"
    headers = {'Cookie': cookie}
    response = requests.get(address, headers=headers)
    return response.content


def user_info(user, cookie):
    address = ''.join(["http://jira/rest/api/2/user?username=", user])
    headers = {'Cookie': cookie}
    response = requests.get(address, headers=headers)
    return response.content


def report_date(user_id, day_num):
    cur_report = get_report_by_user(user_id, day_num)
    if cur_report:
        body = [{'content': cur_report.content, 'date': cur_report.date.strftime("%Y-%m-%d %H:%M:%S"),
                 'issue': cur_report.issue_name,
                 'timeSpent': cur_report.time_spent, 'userid': cur_report.user_id, 'worklogId': cur_report.worklog_id}]
        body = json.dumps(body)
    else:
        body = []
        body = json.dumps(body)
    return body, 200


def make_request_cookie():
    jsessionid = request.cookies['JSESSIONID']
    token = request.cookies['atlassian.xsrf.token']
    cookies = ''.join(['JSESSIONID=', jsessionid, ';atlassian.xsrf.token=', token])
    return cookies


def make_response_cookie(jsessionid, token):
    cookies = ''.join(['JSESSIONID=', jsessionid, ';atlassian.xsrf.token=', token])
    return cookies


def make_user_info(user):
    user_email = user['emailAddress']
    user_id = get_user_id_by_email(user_email)
    group_id = get_group_id_by_user_id(user_id)
    domain_id = get_domain_id_by_user_id(user_id)
    group_name = get_group_name_by_id(group_id)
    domain_name = get_domain_name_by_id(domain_id)
    user['userId'] = user_id
    user['groupName'] = group_name
    user['domainName'] = domain_name
    return user
