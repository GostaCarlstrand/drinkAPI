from flask import Blueprint, render_template

api_blueprint = Blueprint('api_blueprint', __name__, template_folder="templates/api_templates")


@api_blueprint.get('/')
def index():
    return render_template('index.html')
