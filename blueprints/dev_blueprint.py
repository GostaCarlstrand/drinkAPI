import json
from flask import Blueprint, render_template, request
from mongo_handler import insert_user
from models import User
from app import db
import pandas as pd


dev_blueprint = Blueprint('dev_blueprint', __name__)


@dev_blueprint.get('/import')
def import_data():
    drink_data = pd.read_csv('cleaned_drink.csv')
    drink_data.to_sql(name='drinks', con=db.engine, if_exists='append')
    return render_template('dev_signup.html')


@dev_blueprint.get('/signup')
def index():
    return render_template('dev_signup.html')


@dev_blueprint.post('/add_api_user')
def sign_up():
    # Data collected from the html form
    name = request.form['fullname']
    admin = request.form["admin".UniqueID]
    new_user = User(name=name, admin=admin, api=api)
    db.session.add(new_user, admin,)
    db.session.commit()
    # returns the api_key string that is also stored in the database
    api_key = insert_user({'name': name, 'admin': admin})
    return json.dumps({'api_key': api_key})
