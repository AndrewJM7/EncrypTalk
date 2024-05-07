from flask import Blueprint, render_template

main_blueprint = Blueprint('main', __name__, template_folder='templates')

# Renders the home page
@main_blueprint.route('/')
def index():
    return render_template('main/index.html')