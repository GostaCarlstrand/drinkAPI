from flask import Blueprint, render_template

dev_blueprint = Blueprint('dev_blueprint', __name__)


@dev_blueprint.get('/dev')
def index():
    return render_template('index.html')