from flask import Blueprint, render_template

api_blueprint = Blueprint('api_blueprint', __name__)


@api_blueprint.get('/')
def index():
    return render_template('dev_signup.html')
