from flask import Blueprint, render_template

from flask import Blueprint, render_template, jsonify

from controllers.dev_controller import get_user_by_key
from controllers.user_controller import get_all_users, get_user_by_id
from models import User

user_blueprint = Blueprint('user_blueprint', __name__)


def get_users():
    users = get_all_users()
    print()
    return jsonify([User.serialize(user) for user in users])


@user_blueprint.get('/user')
def index():
    temp = get_user_by_key('1E9RNF0TIOW2Z3L')
    print()
    return render_template('dev_signup.html')


@user_blueprint.get('/user/<user_id>')
def profile_get_user(user_id):
    user_id = get_user_by_id(user_id)
    return jsonify([User.serialize(user_id)])

