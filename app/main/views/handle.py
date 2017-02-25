from flask import render_template, request
import requests
from app.main import main
import json
import utils
import jira
from app.main.db.db_controller import *
from flask import Response


@main.route("/", methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route("/api/v1/jira/login", methods=['POST', 'DELETE'])
def jira_login_handler():
    print request.method
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        body = {"username": username, "password": password}
        response = jira.jira_login(body)
        jsessionid = response.cookies['JSESSIONID']
        token = response.cookies['atlassian.xsrf.token']
        cookies = utils.make_response_cookie(jsessionid, token)
        user = utils.user_info(username, cookies)
        user = utils.make_user_info(json.loads(user))
        user = json.dumps(user)
        response = Response(user, status=200)
        response.set_cookie('JSESSIONID', jsessionid)
        response.set_cookie('atlassian.xsrf.token', token)
        response.set_cookie('username', username)
        return response

    else:
        cookies = utils.make_request_cookie()
        headers = {'Cookie': cookies}
        response = jira.jire_logout(headers)
        return response.content, response.status_code


@main.route("/api/v1/jira/user", methods=['GET'])
def login_again():
    if request.cookies:
        cookies = utils.make_request_cookie()
        user = utils.user_info(request.cookies['username'], cookies)
        user = utils.make_user_info(json.loads(user))
        user = json.dumps(user)
        response = Response(user, status=200)
        return response
    else:
        return '', 404


@main.route('/api/v1/report/user/<user_id>/<day_num>')
def report(user_id, day_num):
    return utils.report_date(user_id, day_num)


@main.route('/api/v1/issue/prev/<user_id>')
def history_issues(user_id):
    issue_list = get_history_issues_by_user_id(user_id)
    body = json.dumps(issue_list)
    response = Response(body, status=200)
    return response


@main.route('/api/v1/jira/search', methods=['POST'])
def jira_search_handler():
    cookies = utils.make_request_cookie()
    response = jira.jira_serach(cookies)
    return response.content, response.status_code


@main.route('/api/v1/jira/project', methods=['GET'])
def project():
    cookies = utils.make_request_cookie()
    headers = {"content-type": "application/json", "Cookie": cookies}
    address = "http://jira/rest/api/2/project"
    response = requests.get(address, headers=headers)
    return response.content, response.status_code


@main.route('/api/v1/jira/worklog', methods=['POST'])
def work_log():
    playload = request.get_json(True)
    return jira.jira_work_log(playload)
