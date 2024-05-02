from re import L
from flask import Blueprint, app, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from app import db
from models import User

contacts_blueprint = Blueprint('contacts', __name__, template_folder='templates')

# Function to get all friends of the current user
def get_friends(user):
    # Get all friends of current user
    friends_strings = user.friends.split(',')
    friends = []
    for friend_email in friends_strings:
        friend = User.query.filter_by(email=friend_email).first()
        if friend:
            friends.append(friend)
    return friends

# Render the contacts page
@contacts_blueprint.route('/contacts')
@login_required
def contacts():
    
    # Get all users except the current user
    users = User.query.filter(User.id != current_user.id).all()
    
    # Get all friends of current user
    friends = get_friends(current_user)
    friend_emails = [friend.email for friend in friends]
    
    # Filter out friends from the list of users
    users = [user for user in users if user.email not in friend_emails]
    return render_template('contacts/contacts.html', users=users, friends=friends)

# Add a friend to the current user's friends list
@contacts_blueprint.route('/add_friend/<email>')
@login_required
def add_friend(email):
    
    # Retrieve the user from the database
    potential_friend = User.query.filter_by(email=email).first()

    # Check if the user exists and is not a friend
    if potential_friend and potential_friend.email not in current_user.friends:
        
        # Add the friend's email to the user's friends list
        current_user.friends += potential_friend.email + ','
        
        # Commit the changes to the database
        db.session.commit()
        
        # Retrieve updated list of friends and users
        users = User.query.filter(User.id != current_user.id).all()
        friends = get_friends(current_user)

        # Remove the added friend from the list of users
        users = [user for user in users if user.email != potential_friend.email]

        flash('Friend added successfully!', 'success')  
        return redirect(url_for('contacts.contacts', users=users, friends=friends)) 
    
    else:
        flash('User not found or already a friend!', 'error') 
        return redirect(url_for('contacts.contacts')) 

# Delete a friend from the current user's friends list
@contacts_blueprint.route('/delete_friend/<email>')
@login_required
def delete_friend(email):
    
    # Retrieve the user from the database
    friend = User.query.filter_by(email=email).first()
    
    # Check if the user exists and is a friend
    if friend and friend.email in current_user.friends:
        
        # Delete the friend's email from the user's friends list
        current_user.friends = current_user.friends.replace(friend.email + ',', '')
        
        # Commit the changes to the database
        db.session.commit()
        
        # Retrieve updated list of friends and users
        users = User.query.filter(User.id != current_user.id).all()
        friends = get_friends(current_user)

        # Query the deleted friend again and add it back to the list of users
        deleted_friend = User.query.filter_by(email=email).first()
        if deleted_friend:
            users.append(deleted_friend)

        flash('Friend deleted successfully!', 'success')  
        return redirect(url_for('contacts.contacts', users=users, friends=friends)) 
    else:
        flash('User not found or not a friend!', 'error') 
        return redirect(url_for('contacts.contacts'))
