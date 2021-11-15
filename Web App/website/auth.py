#Authenticated Routes for Website i.e. sites requiring authentication

from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth',__name__)

##Routes

#Redirect
@auth.route('/')
@login_required
def reLink():
    return render_template("home.html",user=current_user)
        

#Login Route
@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        # Get Data from HTML
        email = request.form.get('email')
        password = request.form.get('password')
        
        #Check if user exists on the Database using email
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) #Allows for website to remember user is logged in the current session
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password! Please try again!', category='error')
        else:
            flash("Email does not exist!",category = 'error')
            
    return render_template("login.html",user = current_user)

#Logout Route
@auth.route('/logout')
@login_required #Ensures that route is only accessible if user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#Signup
@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        # Get Data from HTML
        email= request.form.get('email')
        first_name= request.form.get('firstName')
        password1= request.form.get('password1')
        password2= request.form.get('password2')
        
        #Check for any errors and flash if there are
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email)<4: #Check if email is has more than 3 alphanumeric
            flash('Email must be greater than 3 Characters.', category='error')
        elif len(first_name) <2: #check if name has more than 1 letters
            flash('First Name must be more than 1 Character.', category='error')
        elif len(password1)<7: #Check if password is more than 7 alphanumeric
            flash('Password must be at least 7 Characters', category='error')
        elif password1 != password2: #Check if password and confirm password is the same
            flash('Passwords dont\'t match.', category='error')
        else:
            #Add user to DB
            new_user = User(email=email,first_name=first_name,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) #Allows for website to remember user is logged in the current session
            flash("Account Created!", category="success")
            return redirect(url_for("views.home"))
            
    return render_template("sign_up.html", user = current_user)

@auth.route('/user-info')
@login_required
def userInfo():
    return render_template("user_info.html",user = current_user)