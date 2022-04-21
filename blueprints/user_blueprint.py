
from flask import Blueprint, render_template
from db_handler import get_user_by_key
from flask import Blueprint, render_template, jsonify
from controllers.user_controller import get_all_users
from models import User


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.get('/user')
def index():
    temp = get_user_by_key('1E9RNF0TIOW2Z3L')
    print()
    return render_template('dev_signup.html')


def get_users():
    users = get_all_users()
    print()
    return jsonify([User.serialize(user) for user in users])
