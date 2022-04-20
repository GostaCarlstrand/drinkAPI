import json
from flask import Blueprint, render_template, request
from mongo_handler import insert_user


dev_blueprint = Blueprint('dev_blueprint', __name__)


@dev_blueprint.get('/signup')
def index():
    return render_template('dev_signup.html')


@dev_blueprint.post('/add_api_user')
def sign_up():
    # Data collected from the html form
    name = request.form['fullname']
    admin = int(request.form['admin'])

    # returns the api_key string that is also stored in the database
    api_key = insert_user({'name': name, 'admin': admin})
    return json.dumps({'api_key': api_key})
