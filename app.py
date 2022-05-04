from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

db = SQLAlchemy()
admin = Admin()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '123secret'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['JSON_SORT_KEYS'] = False

    admin.init_app(app)
    db.init_app(app)

    from blueprints.api_blueprint import api_blueprint
    from blueprints.user_blueprint import user_blueprint
    from blueprints.open_blueprint import open_blueprint
    app.register_blueprint(api_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(open_blueprint)

    return app


if __name__ == "__main__":
    create_app().run()
