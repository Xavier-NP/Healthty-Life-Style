from flask import Flask, app
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from os import path
from flask_login import LoginManager
import hashlib

#Assigning Database Module
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'GUMMYKKB'
    app.config['SQLALCHEMY_DATABASE_URI'] =f"sqlite:///{DB_NAME}"  #f"postgresql://nujklfeybzgodl:223d4e00a7baa85133eac464de87c2a80c963f15810b38ad88ce6c03e6855c5e@ec2-54-209-221-231.compute-1.amazonaws.com:5432/d7lqkd171p92s5" #Database Storage LOCAL = sqlite:///{DB_NAME} 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app) #Initializing the Database
    
   
    
    #Importing Routes
    from .views import views
    from .auth import auth
    
    #Setting Prefixes
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    #Check if Database file Exists
    from .models import User,Note
    create_database(app)
    
    #Initializing Data into Database
    init_Disabilities(app) 
    
    #Login Manager
    login_manager= LoginManager()
    login_manager.login_view = 'auth.login' #Redirects to login page if trying to access login_required routes
    login_manager.init_app(app)
    
    
    #Defining to the app on how to load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    
    return app


#Initializing Data
    
def init_Disabilities(app):
    from .models import Disability,Doctor,Patient
    disability_names= ["Diabetes","Crutches"] #Ensure that name is EXACTLY THE SAME as checkbox name in sign_up.html
    role_names = ["Patient","Doctor"] #Ensure that name is EXACTLY THE SAME as checkbox name in sign_up.html
    pw = hashlib.sha256()
    ph = "Pa$$w0rd"
    with app.app_context():
        #Disabilities
        check1 = Disability.query.filter_by(id=1).first()
        #check2 = Role.query.filter_by(id=1).first()
        if (not check1) :
            for x in range(len(disability_names)):
                new_disability = Disability(disName=disability_names[x])
                db.session.add(new_disability)
            
            pw.update(ph.encode("utf-8"))
                 
            #Inserting Doctors
            new_doctor = Doctor(
                email="s10208449@connect.np.edu.sg",
                password=pw.digest().hex(),
                full_name= "Xavier Kee",
                )
            
            db.session.add(new_doctor)
            db.session.commit()
            
            new_doctor = Doctor(
                email="s10205561@connect.np.edu.sg",
                password=pw.digest().hex(),
                full_name = 'Dr Sins'
                )
            
            db.session.add(new_doctor)
            db.session.commit()
                
        
    
        
#Creating Database
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
        

        