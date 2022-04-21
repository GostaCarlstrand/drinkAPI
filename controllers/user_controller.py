from models import User


def get_all_users():
    return User.query.filter(User.id).all()


def get_user_by_id(user_id):
    return User.query.filter(User.id == user_id).first()
