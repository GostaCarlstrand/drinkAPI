import json

from flask import Blueprint, render_template, request

dev_blueprint = Blueprint('dev_blueprint', __name__)


@dev_blueprint.get('/signup')
def index():
    return render_template('dev_signup.html')


@dev_blueprint.post('/add_api_user')
def sign_up():
    name = request.form['fullname']
    admin = request.form['admin']
    api_key = {
        'access_key': 123
    }
    return json.dumps(api_key)
