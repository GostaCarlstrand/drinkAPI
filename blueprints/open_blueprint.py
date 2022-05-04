import json
from app import db
import pandas as pd
from flask import Blueprint, render_template, request, flash, redirect, url_for
from controllers.user_controller import insert_user
from models import User

open_blueprint = Blueprint('open_blueprint', __name__)


@open_blueprint.get('/signup')
def index():
    return render_template('dev_signup.html')


@open_blueprint.post('/signup')
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


@open_blueprint.get('/import')
def import_data():
    drink_data = pd.read_csv('cleaned_drink.csv')
    drink_data.to_sql(name='drinks', con=db.engine, if_exists='append')
    return render_template('dev_signup.html')