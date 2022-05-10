"""
Drink Flask API with over 500 drinks
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
admin = Admin()


SWAGGER_URL = '/swagger'
SWAGGER_JSON = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint (
    SWAGGER_URL,
    SWAGGER_JSON,
    config={
        'app_name': 'Drink API database'
    }

)


def create_app():
    """
    Factory function for flask application
    :return: app object
    """
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
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)
    return app


if __name__ == "__main__":
    create_app().run()
