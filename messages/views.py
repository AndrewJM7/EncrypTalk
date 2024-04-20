from flask import Blueprint, render_template

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')


@messages_blueprint.route('/messages')
def messages():
    return render_template('messages/messages.html')