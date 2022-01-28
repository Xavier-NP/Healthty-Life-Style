#Authenticated Routes for Website i.e. sites requiring authentication

import re
from flask import Blueprint,render_template,request,flash,redirect,url_for
from flask.helpers import send_file
from sqlalchemy.sql.functions import user
from .models import Disability, Doctor,Patient, User,CalsBMI
import hashlib
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import datetime
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from io import BytesIO, StringIO
import base64





auth = Blueprint('auth',__name__)
NoneType=type(None)
pw = hashlib.sha256()
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
            if check_pw(user,password):
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

#Sign-up Route
@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method =='POST':
        # Get Data from HTML
        
        first_name= request.form.get('firstName')
        last_name= request.form.get('lastName')
        email= request.form.get('email')
        mobileNum = request.form.get('mobileNum')
        nric = request.form.get('nric')
        addr = request.form.get('addr')
        password1= request.form.get('password1')
        password2= request.form.get('password2')
        disabilities = request.form.getlist('disability')
        doctor = request.form.get('doctor')
        
        #Check for any errors and flash if there are
        user = Patient.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif len(email)<4: #Check if email is has more than 3 alphanumeric
            flash('Email must be greater than 3 Characters.', category='error')
        elif len(first_name) <2: #check if first name has more than 1 letters
            flash('First Name must be more than 1 Character.', category='error')
        elif len(last_name) <2: #check if last name has more than 1 letters
            flash('Last Name must be more than 1 Character.', category='error')
        elif len(mobileNum)!=8 or (mobileNum.isnumeric()==False):#ensure number is 8 digits, mobile number is numeric
            flash('Enter a valid 8 digit mobile number', category = 'error')
        elif len(nric)!=9:#ensure ic entered is 9 char
            flash('Enter a valid NRIC/FIN')
        elif len(password1)<7: #Check if password is more than 7 alphanumeric
            flash('Password must be at least 7 Characters', category='error')
        elif password1 != password2: #Check if password and confirm password is the same
            flash('Passwords dont\'t match.', category='error')
        elif not disabilities: #Check if at least 1 disability is selected
            flash('Please select a disability!',category='error')
        else:
            pw.update(password1.encode("utf-8"))
            #Creating New user
            new_user = Patient(first_name=first_name,
                            last_name=last_name, 
                            email=email, 
                            mobileNum=mobileNum, 
                            nric=nric, addr=addr, 
                            password=pw.digest().hex(),
                            doctor_id=doctor
                            #role_id=1 # Setting all users that login to be Patients
                            )
            
            #Assigning disabilities to user
            for x in range(len(disabilities)):
                dist_name=Disability.query.filter_by(disName=disabilities[x]).first()
                new_user.disabilities.append(dist_name)
            
            
            #Adding created user to DB
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True) #Allows for website to remember user is logged in the current session
            flash("Account Created!", category="success")
            return redirect(url_for("views.home"))
            
    return render_template("sign_up.html", user = current_user)

#User-Info Route
@auth.route('/user-info')
@login_required
def userInfo():
    return render_template("user_info.html",user = current_user)



def getBMI(w,h):
    bmi = round((w/((h/100)**2)),2)
    return bmi
    


#Calculate BMI
@auth.route('/bmi',methods=['GET','POST'])
@login_required
def calBMI():#bmi = kg/m^2
    if request.method == 'POST' and request.form.get('weight').isnumeric() and request.form.get('height').isnumeric():
        w = float(request.form.get('weight'))
        h = float(request.form.get('height'))
        bmi = getBMI(w,h)

        return render_template("bmi.html",bmi = bmi,user=current_user)
    else:
        return render_template("bmi.html",bmi=0,user = current_user)


@auth.route('/calories',methods = ['GET','POST'])
@login_required
def calories():
    if request.method == 'POST' and request.form.get('weight')!="" and request.form.get('age')!=""and request.form.get('age')!="":
        w = float(request.form.get('weight'))
        h = float(request.form.get('height'))
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        activeness = request.form.get('activeness')
        bmr = 0
        calNeed = 0
        if gender == "male":
            bmr = 88.362 + (13.397*w)+(4.799*h)-(5.677*age)
        elif gender == "female":
            bmr = 447.593 + (9.247*w) + (3.098*h)-(4.330*age)
        if(activeness == "1"):
            calNeed = bmr*1.2
        elif(activeness == "2"):
            calNeed = bmr*1.37
        elif(activeness == "3"):
            calNeed = bmr*1.55
        elif(activeness=="4"):
            calNeed = bmr*1.725
        elif(activeness=="5"):
            calNeed = bmr*1.9
        calNeed = round(calNeed,2)
        bmi = getBMI(w,h)
    else:
        calNeed = 0
        bmi = 0

        #intake
    if request.method=="POST" and request.form.get("breakfast")!=NoneType and request.form.get("lunch")!=NoneType and request.form.get("dinner")!=NoneType: 
        chickenRice = 607 #https://www.healthhub.sg/live-healthy/165/healthy_cooking
        wontonNoodle = 409 #https://www.thestar.com.my/lifestyle/viewpoints/tell-me-about/2011/02/27/malaysian-calories
        duckRice = 673 #https://www.healthxchange.sg/food-nutrition/food-tips/best-worst-singapore-hawker-chinese-food-duck-rice-fishball-noodle
        meal = [chickenRice,wontonNoodle,duckRice]

        #Serving size in quantity
        try:
            bServing = int(request.form.get('bServing'))
        except:
            bServing = 1
        try:
            lServing = int(request.form.get('lServing'))
        except:
            lServing = 1
        try:
            dServing = int(request.form.get('dServing'))
        except:
            dServing=1
        ##

        try:
            breakfast = int(request.form.get('breakfast'))
            lunch = int(request.form.get('lunch'))
            dinner = int(request.form.get('dinner'))
            totalIntake = ((meal[breakfast]*bServing)+(meal[lunch]*lServing)+(meal[dinner]*dServing))
        except:
            totalIntake=0
    else:
        totalIntake=0
    if bmi!=0 and totalIntake!=0:
        dateNow = datetime.datetime.now().date()
        #dateNow=datetime.date(2021, 11, 14)#place data into the db to test
        exist = CalsBMI.query.filter_by(CalsBMIdate = dateNow).first()
        if exist:# if the date already exists
            flash(f'You can record BMI and Calories input once per day! [{exist.calories} kcals and BMI of {exist.bmi} recorded]',category='error')
        else:
            new_CalsBMI = CalsBMI(calories = totalIntake, bmi = bmi, CalsBMIdate = dateNow, CalsBMIid = current_user.id)
            db.session.add(new_CalsBMI)
            db.session.commit()
            flash('Your BMI and Calories input has been recorded',category='success')

    return render_template("calories.html",calNeed = calNeed, totalIntake = totalIntake,bmi=bmi,user = current_user)


@auth.route('/health-trend',methods = ['GET','POST'])
@login_required
def health_trend():
    data = CalsBMI.query.order_by(CalsBMI.CalsBMIdate).all()
    #commented data are for testing
    dateList = []
    caloriesList = []
    bmiList = []
    #dateList = ['12 Jan','13 Jan','14 Jan','15 Jan','16 Jan','17 Jan','18 Jan']
    #caloriesList = [2100,2200,2300,2400,2300,2200,2000]
    #bmiList = [21,21.5,22,22,20,21,20]
    for i in data:#append data into list for visualisation
        dateList.append(i.CalsBMIdate)
        caloriesList.append(i.calories)
        bmiList.append(i.bmi)
    
    #create plot
    fig = plt.figure(figsize=(10,8),constrained_layout=True)
    gs = GridSpec(nrows=2,ncols=2,figure = fig)
    ax1 = fig.add_subplot(gs[0,:])
    ax1.plot(dateList,bmiList,'b-o',label = 'BMI')
    ax1.set_title('BMI Trend', fontsize=15)
    ax1.set_xlabel('Date')
    ax1.set_ylabel('BMI')
    ax1.set_ylim(bottom = 0, top = round(max(bmiList)+5))
    #ax1.legend(loc='upper right')


    ax2 = fig.add_subplot(gs[1,:])
    ax2.plot(dateList, caloriesList, 'r-+', label='Calories Intake')
    ax2.set_title('Calories Intake', fontsize=15)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Calories Intake')
    ax2.set_ylim(bottom=0,top = round(max(caloriesList)+1000))
    #ax2.legend(loc='lower right')
    
    fig.suptitle("Dashboard for health trends",fontsize = 25)

    #fig.savefig('website/static/health_trend.png',dpi=300)
    plt.show()

    return render_template("health_trend.html",user = current_user)


#Check User Password if correct Function
def check_pw(user,e_pw):
        ph = hashlib.sha256()
        ph.update(e_pw.encode("utf-8"))
        hashed_pw = ph.digest().hex()
        if user.password==hashed_pw:
            return True
        else:
            return False    
    
