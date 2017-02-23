from flask import render_template, request
import requests
from app.main import main
import json
import utils
from app.main.db.db_controller import *
from flask import Response


@main.route("/", methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route("/api/v1/jira/login", methods=['POST', 'DELETE'])
def jira_login():
    address = 'http://jira/rest/auth/1/session'
    print request.method
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        body = {"username": username, "password": password}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(address, headers=headers, data=json.dumps(body))
        jsessionid = response.cookies['JSESSIONID']
        token = response.cookies['atlassian.xsrf.token']
        cookies = utils.make_cookie(jsessionid, token)
        # login_info(cookies)
        user = utils.user_info(username, cookies)
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
        response = Response(user, status=200)
        response.set_cookie('JSESSIONID', jsessionid)
        response.set_cookie('atlassian.xsrf.token', token)
        response.set_cookie('username', username)
        return response

    else:
        cookies = utils.make_cookie(request.cookies['JSESSIONID'], request.cookies['atlassian.xsrf.token'])
        headers = {'Cookie': cookies}
        print headers
        response = requests.delete(address, headers=headers)
        return response.content, response.status_code


@main.route("/api/v1/jira/user", methods=['GET'])
def login_again():
    if request.cookies:
        cookies = utils.make_cookie(request.cookies['JSESSIONID'], request.cookies['atlassian.xsrf.token'])
        user = utils.user_info(request.cookies['username'], cookies)
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
        return '', 404


@main.route('/api/v1/report/user/<user_id>/<day_num>')
def report(user_id, day_num):
    return utils.report_date(user_id, day_num)


@main.route('/api/v1/issue/prev/<user_id>')
def history_issues(user_id):
    issue = get_history_issues_by_user_id(user_id)
    body = [{'issue': issue, 'user_id': user_id}]
    body = json.dumps(body)
    return body, 200


@main.route('/api/v1/jira/search', methods=['POST'])
def jira_search():
    cookies = utils.make_cookie(request.cookies['JSESSIONID'], request.cookies['atlassian.xsrf.token'])
    playload = request.get_json(True)
    address = "http://jira/rest/api/2/search"
    headers = {"content-type": "application/json", "Cookie": cookies}
    response = requests.post(address, headers=headers, json=playload, proxies={'http': 'http://localhost:8888'})
    return response.content, response.status_code


@main.route('/api/v1/jira/project', methods=['GET'])
def project():
    cookies = utils.make_cookie(request.cookies['JSESSIONID'], request.cookies['atlassian.xsrf.token'])
    headers = {"content-type": "application/json", "Cookie": cookies}
    address = "http://jira/rest/api/2/project"
    response = requests.get(address, headers=headers)
    return response.content, response.status_code
