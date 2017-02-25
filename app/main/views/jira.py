from flask import request, Response, make_response
import json
import requests
import time
import utils
import datetime
from app.main.db.db_controller import *


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


def jira_work_log(data):
    user_id = data['userId']
    login_id = data['loginId']
    user_name = data['username']
    create = data['create']
    update = data['update']
    delete = data['delete']
    if 'datetime' in data.keys():
        date_time = data['datetime']
    else:
        date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print 'create :', create
    report_update = update_reports(update, user_id, login_id, user_name, date_time)
    report_create = create_reports(create, user_id, login_id, user_name, date_time)
    if report_update and report_create:
        response = report_create + report_update
    elif report_create:
        response = report_create
    else:
        response = report_update
    return json.dumps(response), 200


def create_reports(create_list, user_id, login_id, user_name, date_time):
    create_response = []
    for issue in create_list:
        key = issue['key']
        spend = issue['timeSpent']
        response = work_log(issue)
        if response.status_code == 201:
            data = json.loads(response.content)
            work_log_id = data['id']
            content = data['comment']
            create_issue_report(user_id, content, date_time, spend, key, work_log_id)
            day_num = datetime.date.today().toordinal() + 365
            create_history_issue(user_id, key, day_num, date_time)
            # TODO CRL ADD
            tmp_response = [{'issue': key, 'id': work_log_id}]
            create_response = create_response + tmp_response
        return create_response


def update_reports(update_list, user_id, login_id, user_name, date_time):
    if update_list:
        update_response = []
        for issue in update_list:
            work_log_id = issue['id']
            key = issue['key']
            response = edit_log(issue)
            if response.status_code == 200:
                content = issue['comment']
                if 'timeSpent' in issue:
                    time_spent = issue['timeSpent']
                else:
                    time_spent = 8
                update_issue_report(content, date_time, time_spent, work_log_id)
                # TODO UPDATE_CRL
                tmp_response = [{'issue': key, 'id': work_log_id}]
                update_response = update_response + tmp_response
            elif response.status_code == 400:
                # TODO DELETE DDRT REPORT
                pass
            else:
                pass
        return update_response


def delete_reports(delete_list, user_id):
    for issue in delete_list:
        issue_id = issue['key']
        log_id = issue['id']


def work_log(create_obj):
    cookies = utils.make_request_cookie()
    headers = {"content-type": "application/json", "Cookie": cookies}
    issue_id = create_obj['key']
    url = 'http://jira/rest/api/2/issue/%s/worklog' % issue_id
    del create_obj['key']
    result = requests.post(url, headers=headers, json=create_obj)
    return result


def edit_log(update_obj):
    cookies = utils.make_request_cookie()
    headers = {"content-type": "application/json", "Cookie": cookies}
    issue_id = update_obj['key']
    log_id = update_obj['id']
    url = 'http://jira/rest/api/2/issue/%s/worklog/%s' % (issue_id, log_id)
    del update_obj['key']
    result = requests.put(url, headers=headers, json=update_obj)
    return result


def delete_log(issue_id, log_id):
    cookies = utils.make_request_cookie()
    headers = {"Cookies": cookies}
    url = 'http://jira/rest/api/2/issue/%s/worklog/%s' % (issue_id, log_id)
    pass
