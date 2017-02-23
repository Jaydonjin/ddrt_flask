def get_history_issue(items):
    max_num = 0
    for item in items:
        if item.day_num >= max_num:
            max_num = item.day_num
            max_issue = item
    return max_issue
