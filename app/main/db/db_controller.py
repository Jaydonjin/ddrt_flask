from db import users, groups_users, groups, domains, history_issues, reports
from app import db
import datetime


def get_user_id_by_email(email):
    user = db.session.query(users).filter(users.email == email).first()
    user_id = user.id
    return user_id


def get_group_id_by_user_id(user_id):
    item = db.session.query(groups_users).filter(groups_users.user_id == user_id).first()
    group_id = item.group_id
    return group_id


def get_domain_id_by_user_id(user_id):
    item = db.session.query(groups_users).filter(groups_users.user_id == user_id).first()
    domain_id = item.domain_id
    return domain_id


def get_group_name_by_id(group_id):
    item = db.session.query(groups).filter(groups.id == group_id).first()
    group_name = item.name
    return group_name


def get_domain_name_by_id(domain_id):
    item = db.session.query(domains).filter(domains.id == domain_id).first()
    domain_name = item.name
    return domain_name


def get_history_issues_by_user_id(user_id):
    item = db.session.query(history_issues).filter(history_issues.user_id == user_id).first()
    issue_key = item.issue_key
    return issue_key


def get_report_by_user(user_id, day_num):
    day_num = int(day_num)
    now = datetime.datetime.now()
    end = now + datetime.timedelta(days=day_num)
    start = now.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    print ('start :', start, ' end :', end)
    item = db.session.query(reports).filter(reports.user_id == user_id).filter(reports.date >= start).filter(
        reports.date < end).first()
    print item.content, item.date
    return item
