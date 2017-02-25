from db import users, groups_users, groups, domains, history_issues, reports
from app import db
from db_utils import *
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
    max_day_num = db.session.query(db.func.max(history_issues.day_num)).scalar()
    items = db.session.query(history_issues).filter(history_issues.user_id == user_id).filter(
        history_issues.day_num == max_day_num).all()
    item_list = []
    for item in items:
        tmp = {'issue': item.issue_key, 'user_id': item.user_id}
        item_list.append(tmp)
    return item_list


def get_report_by_user(user_id, day_num):
    day_num = int(day_num)
    now = datetime.datetime.now()
    end = now + datetime.timedelta(days=day_num)
    start = now.strftime("%Y-%m-%d")
    end = end.strftime("%Y-%m-%d")
    items = db.session.query(reports).filter(reports.user_id == user_id).filter(reports.date >= start).filter(
        reports.date < end).all()
    if items:
        items_list = []
        for item in items:
            items_list.append(item)
        return items_list
    else:
        return None


def create_issue_report(user_id, content, date, spend, key, work_log_id):
    max_id = db.session.query(db.func.max(reports.id)).scalar()
    report_id = max_id + 1
    report = make_create_report(int(report_id), int(user_id), content, date, spend, key, int(work_log_id))
    db.session.add(report)
    db.session.commit()


def update_issue_report(content, date, spend, work_log_id):
    report = reports.query.filter_by(worklog_id=work_log_id).first()
    report.content = content
    report.date = date
    report.time_spent = spend
    db.session.commit()


def create_history_issue(user_id, key, day_num, date):
    max_id = db.session.query(db.func.max(history_issues.id)).scalar()
    issue_id = max_id + 1
    issue = make_create_history_issue(int(issue_id), int(user_id), key, int(day_num), date)
    db.session.add(issue)
    db.session.commit()
