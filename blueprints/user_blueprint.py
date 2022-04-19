from flask import Blueprint, render_template

user_blueprint = Blueprint('user_blueprint', __name__, template_folder="templates/user_templates")


@user_blueprint.get('/user')
def index():
    return render_template('user_index.html')