from flask import current_app
from flask import render_template

from app.main import main


@main.route("/version", methods=['GET'])
def version():
    return render_template('main/version.html', version=current_app.config['VERSION'])


@main.route("/faq.htm")
def faq():
    return render_template('main/faq.html')
