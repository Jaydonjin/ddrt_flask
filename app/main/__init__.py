from flask import Blueprint

url_prefix = '/ddrt'
main = Blueprint('main', __name__, url_prefix=url_prefix, static_folder='static', static_url_path='/static')

from . import views
from . import db
