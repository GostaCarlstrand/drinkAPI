import json
from app import db
import pandas as pd
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, Response

from blueprints.api_blueprint import authorize_api_key
from controllers.api_controller import api_usage
from controllers.user_controller import get_all_users, get_user_by_id, insert_user
from models import User


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.before_request
@authorize_api_key
def before_request():
    endpoint = request.base_url
    api_key = request.headers.get('api_key')
    api_usage(api_key, endpoint)


@user_blueprint.get('/api/v1/user')
@authorize_api_key
def get_users():
    users = get_all_users()
    return jsonify([User.serialize(user) for user in users])


@user_blueprint.get('/api/v1/user/<user_id>')
@authorize_api_key
def profile_get_user(user_id):
    if user_id.isdigit():
        user_id = int(user_id)
    else:
        return Response(json.dumps({'Error': 'Id must be an integer'}), 400, content_type='application/json')

    user_id = get_user_by_id(user_id)

    if not user_id:
        return Response(json.dumps({'Error': f'User is not present in the database'}),
                        404, content_type='application/json')

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

    user = User.query.filter_by(name=name).first()
    if user:
        flash('Name already in use', 'error')
        return redirect(url_for('user_blueprint.index'))

    admin = int(request.form["admin"])
    api_key = insert_user({'name': name, 'admin': admin})

    return json.dumps({'api_key': api_key})

