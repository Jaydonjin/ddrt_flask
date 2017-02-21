from flask import Blueprint

url_prefix = '/ddrt_flask'
main = Blueprint('main', __name__, url_prefix=url_prefix, static_url_path='/')

from . import views
from . import db
