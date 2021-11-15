from logging import NullHandler
import re
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        contact = request.form.get('contact')
        password = request.form.get('password')

        user = User.query.filter_by(contact=contact).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        contact = request.form.get('contact')
        email = request.form.get('email')
        fName = request.form.get('fName')
        icnumber = request.form.get('icnumber')
        password = request.form.get('password')
        cpassword = request.form.get('cpassword')

        user = User.query.filter_by(contact=contact).first()
        if user:
            flash('Mobile number alreadt exists',category = 'error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(fName) < 2:
            flash('Full name must be greater than 1 character.', category='error')
        elif len(icnumber) != 9:
            flash('Please enter a vlid IC number', category = 'error')
        elif password != cpassword:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else: 
            new_user = User(contact = contact, email=email, fName=fName, icnumber = icnumber, password=generate_password_hash(
                password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.userInfo'))
    return render_template("sign_up.html")

@auth.route('/userinfo')
@login_required
def userInfo():
    return render_template("userInfo.html")


