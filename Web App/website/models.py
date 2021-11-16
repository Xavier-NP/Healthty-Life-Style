from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
##Defining Schemas

#Class User
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    mobileNum = db.Column(db.String(8))
    nric = db.Column(db.String(9))
    notes = db.relationship('Note')
    
#Class Notes
class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
#Doctor/Caregiver, Disability