import requests, json
from ..db.db_controller import *


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


def make_cookie(jsessionid, token):
    cookies = ''.join(['JSESSIONID=', jsessionid, ';atlassian.xsrf.token=', token])
    return cookies
