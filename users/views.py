from flask import Blueprint, redirect, render_template
from users.forms import RegisterForm, LoginForm
import bcrypt
from flask import Blueprint, render_template, redirect, url_for, flash
from app import db
from models import User
from flask_login import login_user
from datetime import datetime

users_blueprint = Blueprint('users', __name__, template_folder='templates')

@users_blueprint.route('/login')
def login():
    return render_template('users/login.html')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(username=form.username.data).first()

        if user:
            flash('Email address already exists')
            return render_template('users/register.html', form=form)
    
        if username:
            flash('Username already exists')
            return render_template('users/register.html', form=form)

        # create a new user with the form data
        new_user = User(email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data,
                        username=form.username.data,
                        password=form.password.data,
                        role='user')

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


@users_blueprint.route('/profile')
def profile():
    return render_template('users/profile.html')