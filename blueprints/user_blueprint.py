from flask import Blueprint, jsonify, request, Response
from app import db
from blueprints.api_blueprint import authorize_api_key
from controllers.api_controller import api_usage
from controllers.user_controller import get_all_users, get_user_by_key, user_check, check_user_keys
from models import User


user_blueprint = Blueprint('user_blueprint', __name__)

@user_blueprint.before_request
@authorize_api_key
def before_request():
    endpoint = request.base_url
    api_key = request.headers.get('api_key')
    api_usage(api_key, endpoint)


@user_blueprint.get('/api/v1/user/')
def get_users():
    list_users = []
    all_users = get_all_users()
    for user in all_users:
        user.__dict__.pop('_sa_instance_state')
        list_users.append(user.__dict__)

    return jsonify({'Drinks': list_users})


@user_blueprint.get('/api/v1/user/<user_id>')
def profile_get_user(user_id):
    user = user_check(user_id)
    return jsonify([User.serialize(user)])


@user_blueprint.put('/api/v1/user/<user_id>')
def update_user(user_id):
    user = user_check(user_id)
    api_key = request.headers.get('api_key')
    user_key = get_user_by_key(api_key)

    update_user_info = request.json
    response = check_user_keys(update_user_info)
    if response:
        return response

    if user == user_key:
        user.name = update_user_info['name']
        user.admin = update_user_info['admin']
        user.api_key = update_user_info['api_key']
        db.session.commit()

    return Response("'Status':'User updated'", 200, content_type='application/json')

