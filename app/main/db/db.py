from app import db


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    type = db.Column(db.Enum('R', 'NR'))
    user_name = db.Column(db.String(45))


class groups_users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    receive_type = db.Column(db.Enum('to', 'cc', 'bc'))
    domain_id = db.Column(db.Integer)


class domains(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    group_id = db.Column(db.Integer)


class groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    template = db.Column(db.String(100))
    scheduling_name = db.Column(db.String(45))


class history_issues(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_key = db.Column(db.String(50))
    user_id = db.Column(db.Integer)
    day_num = db.Column(db.Integer)
    create_at = db.Column(db.DateTime)


class reports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    content = db.Column(db.String(1000))
    date = db.Column(db.String(45))
    time_spent = db.Column(db.String(45))
    issue_name = db.Column(db.String(45))
    worklog_id = db.Column(db.Integer)

    def get_dict(self):
        dct = self.__dict__
        del dct['_sa_instance_state']
        return dct
