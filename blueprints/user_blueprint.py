from flask import Blueprint, render_template

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.get('/user')
def index():
    return render_template('index.html')