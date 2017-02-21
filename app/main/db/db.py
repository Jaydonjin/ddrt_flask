from app import db


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    type = db.Column(db.Enum('R', 'NR'))
    user_name = db.Column(db.String(45))

    def get_dict(self):
        dct = self.__dict__
        return dct
