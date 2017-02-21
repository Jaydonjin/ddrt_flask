from flask_sqlalchemy import SQLAlchemy
from app.main import main

main.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@10.16.76.245:3306/ddrt_jira_dev'
db = SQLAlchemy(main)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    type = db.Column(db.Enum('R', 'NR'))
    user_name = db.Column(db.String(45))

    def get_dict(self):
        dct = self.__dict__
        return dct
