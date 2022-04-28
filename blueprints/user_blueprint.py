import json
from app import db
import pandas as pd
from flask import Blueprint, render_template, jsonify, request
from controllers.user_controller import get_all_users, get_user_by_id, insert_user
from models import User


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.get('/api/v1/user')
def get_users():
    users = get_all_users()
    return jsonify([User.serialize(user) for user in users])


@user_blueprint.get('/api/v1/user/<user_id>')
def profile_get_user(user_id):
    user_id = get_user_by_id(user_id)
    return jsonify([User.serialize(user_id)])


@user_blueprint.get('/import')
def import_data():
    drink_data = pd.read_csv('cleaned_drink.csv')
    drink_data.to_sql(name='drinks', con=db.engine, if_exists='append')
    return render_template('dev_signup.html')


@user_blueprint.get('/signup')
def index():
    return render_template('dev_signup.html')


@user_blueprint.post('/signup')
def sign_up():
    # Data collected from the html form
    name = request.form['fullname']
    admin = int(request.form["admin"])
    api_key = insert_user({'name': name, 'admin': admin})
    return json.dumps({'api_key': api_key})

