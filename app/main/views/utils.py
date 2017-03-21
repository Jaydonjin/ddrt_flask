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
    data = get_report_by_user(user_id, day_num)
    if data:
        body = make_report_data(data)
        body = json.dumps(body)
        print body
    else:
        body = []
        body = json.dumps(body)
    return body, 200


def make_request_cookie():
    if 'JSESSIONID' in request.cookies.keys() and 'atlassian.xsrf.token' in request.cookies.keys():
        jsessionid = request.cookies['JSESSIONID']
        token = request.cookies['atlassian.xsrf.token']
        cookies = ''.join(['JSESSIONID=', jsessionid, ';atlassian.xsrf.token=', token])
        return cookies
    else:
        return None


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


def make_report_data(data):
    result_list = []
    for cur_report in data:
        tmp_report = {'content': cur_report.content, 'date': cur_report.date.strftime("%Y-%m-%d %H:%M:%S"),
                      'issue': cur_report.issue_name,
                      'timeSpent': cur_report.time_spent, 'userid': cur_report.user_id,
                      'worklogId': cur_report.worklog_id}
        result_list.append(tmp_report)
    return result_list


def joint_list(list1, list2):
    for item in list2:
        list1.append(item)
    return list1
