from flask import Blueprint, render_template, jsonify
from controllers.user_controller import get_all_users
from models import User


user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.get('/user')
def get_users():
    users = get_all_users()
    print()
    return jsonify([User.serialize(user) for user in users])
