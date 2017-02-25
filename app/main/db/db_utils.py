from db import reports, history_issues


def make_create_report(id, user_id, content, date, spend, key, work_log_id):
    temp_report = reports()
    temp_report.id = id
    temp_report.user_id = user_id
    temp_report.content = content
    temp_report.date = date
    temp_report.time_spent = spend
    temp_report.issue_name = key
    temp_report.worklog_id = work_log_id
    return temp_report


def make_create_history_issue(item_id, user_id, key, day_num, date):
    temp_issue = history_issues()
    temp_issue.id = item_id
    temp_issue.user_id = user_id
    temp_issue.issue_key = key
    temp_issue.day_num = day_num
    temp_issue.create_at = date
    return temp_issue
