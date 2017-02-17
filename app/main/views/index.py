from flask import render_template

from app.main import main
from app.models import Book


@main.route("/", methods=['GET'])
def index():
    book = Book('The Art of Computer Programming ')
    return render_template('main/index.html', book=book)
