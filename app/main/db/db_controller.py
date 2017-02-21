from db import users
from app import db


def get_userId_by_email(email):
    user = db.session.query(users).filter(users.email == email).all()
    return user
