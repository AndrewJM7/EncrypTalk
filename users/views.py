from flask import Blueprint, redirect, render_template
from users.forms import RegisterForm, LoginForm
import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from models import User
from flask_login import login_user, logout_user, login_required

users_blueprint = Blueprint('users', __name__, template_folder='templates')

#  Logs in the user
@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        # check if user exists and the password is correct 
        if not user or not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            flash('Please check your login details and try again.')
            return render_template('users/login.html', form=form)
        
        login_user(user)

        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('messages.rooms'))
        
    return render_template('users/login.html', form=form)

# Registers a new user
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()

    if form.validate_on_submit():
        
        user = User.query.filter_by(email=form.email.data).first()

        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        password=form.password.data)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)

# Logs out the user
@users_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))