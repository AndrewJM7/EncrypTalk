from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_socketio import send, join_room, leave_room, emit, disconnect
from app import socketio
from contacts.views import get_friends
from models import User

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')
    
# Renders chat page
@messages_blueprint.route('/chat/<friend_email>')
@login_required
def chat(friend_email):
    friend = User.query.filter_by(email=friend_email).first()
    return render_template('messages/chat.html', friend=friend)

# Renders room page
@messages_blueprint.route('/rooms')
@login_required
def rooms():
    friends = get_friends(current_user)
    return render_template('messages/rooms.html', friends=friends)



