from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from flask_socketio import send, join_room, leave_room, emit, disconnect
from app import socketio
from contacts.views import get_friends
from models import User
import hashlib

messages_blueprint = Blueprint('messages', __name__, template_folder='templates')
    
# Function to generate unique chat room ID
def generate_id(email1, email2):
    # Sort the emails alphabetically to ensure consistency
    sorted_emails = sorted([email1, email2])
    # Concatenate the sorted emails
    concat_emails = ''.join(sorted_emails)
    # Generate a unique hash for the concatenated emails
    chat_room_id = hashlib.md5(concat_emails.encode()).hexdigest()
    return chat_room_id

# Renders chat page
@messages_blueprint.route('/chat/<friend>')
@login_required
def chat(friend):
    friend = User.query.filter_by(email=friend).first()
    return render_template('messages/chat.html', friend=friend)

# Renders room page
@messages_blueprint.route('/rooms')
@login_required
def rooms():
    friends = get_friends(current_user)
    return render_template('messages/rooms.html', friends=friends, generate_id=generate_id)

# Allows the user to send a message
@socketio.on('send_message')
def handle_message(data):
    message = data['message']
    sender_email = current_user.email
    emit('message', {'message': f'{message}', 'sender': sender_email}, broadcast=True)


