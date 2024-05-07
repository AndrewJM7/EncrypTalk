from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_socketio import send, join_room, leave_room, emit, disconnect
from app import socketio
from contacts.views import get_friends
from models import User
import hashlib

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')

# Sort the emails to ensure a consistent room name
def get_room_name(user1, user2):
    emails = sorted([user1, user2])
    room_id = hashlib.sha256(''.join(emails).encode()).hexdigest()
    return room_id

# Renders chat page
@messages_blueprint.route('/chat/<friend>')
@login_required
def chat(friend):
    friend = User.query.filter_by(email=friend).first()
    room_id = get_room_name(current_user.email, friend.email)
    return render_template('messages/chat.html', friend=friend, room_id=room_id)

# Renders room page
@messages_blueprint.route('/rooms')
@login_required
def rooms():
    friends = get_friends(current_user)
    return render_template('messages/rooms.html', friends=friends)

# Allows the user to send a message
@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    room_id = data['room_id']
    sender_email = current_user.email
    emit('message', {'message': f'{message}', 'sender': sender_email}, room=room_id)

# Allows the user to join a room
@socketio.on('join_room')
def join_room_handler(data):
    room_id = data['room_id']
    join_room(room_id)

# Allows the user to leave a room
@socketio.on('leave_room')
def leave_room_handler(data):
    room_id = data['room_id']
    leave_room(room_id)

