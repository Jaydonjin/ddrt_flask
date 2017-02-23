from flask import Blueprint

url_prefix = '/ddrt'
main = Blueprint('main', __name__, url_prefix=url_prefix, static_url_path='/ddrt_flask')

from . import views
from . import db
