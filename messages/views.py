from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from flask_socketio import send, join_room, leave_room, emit, disconnect
from app import socketio
from contacts.views import get_friends
from models import User

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')


@messages_blueprint.route('/messages')
@login_required
def messages():
    return render_template('messages/messages.html')


@messages_blueprint.route('/rooms')
@login_required
def rooms():
    friends = get_friends(current_user)
    return render_template('messages/rooms.html', friends=friends)


