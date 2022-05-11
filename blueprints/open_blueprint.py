"""
End points that do not require any auth
"""
import json
import pandas as pd
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import db
from controllers.user_controller import insert_user
from models import User

open_blueprint = Blueprint('open_blueprint', __name__)


@open_blueprint.get('/signup')
def index():
    """
    Get the signup page
    :return: HTML doc
    """
    return render_template('dev_signup.html')


@open_blueprint.post('/signup')
def sign_up():
    """
    Collect data from the user and store it in the database
    :return: User api key
    """
    # Data collected from the html form
    name = request.form['fullname']

    user = User.query.filter_by(name=name).first()
    if user:
        flash('Name already in use', 'error')
        return redirect(url_for('open_blueprint.index'))

    admin = int(request.form["admin"])
    api_key = insert_user({'name': name, 'admin': admin})

    return json.dumps({'api_key': api_key})


@open_blueprint.get('/import')
def import_data():
    """
    Get all drinks from the db.
    :return: HTML doc
    """
    drink_data = pd.read_csv('cleaned_drink.csv')
    drink_data.to_sql(name='drinks', con=db.engine, if_exists='append')
    return render_template('dev_signup.html')
