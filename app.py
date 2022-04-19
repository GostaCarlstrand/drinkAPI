from flask import Flask
from blueprints.api_blueprint import api_blueprint
from blueprints.user_blueprint import user_blueprint

app = Flask(__name__)
app.register_blueprint(api_blueprint)
app.register_blueprint(user_blueprint)


if __name__ == "__main__":
    app.run()
