def get_all_users():
    from models import User
    return User.query.filter(User.id).all()
