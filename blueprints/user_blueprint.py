from flask import Blueprint, render_template

from flask import Blueprint, render_template, jsonify


from controllers.user_controller import get_all_users, get_user_by_id, get_user_by_key
from models import User

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.get('/user')
def get_users():
    users = get_all_users()
    return jsonify([User.serialize(user) for user in users])


@user_blueprint.get('/user/<user_id>')
def profile_get_user(user_id):
    user_id = get_user_by_id(user_id)
    return jsonify([User.serialize(user_id)])

