from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

##Defining Schemas

#Class Disability
ailments = db.Table('ailment',
        db.Column('user_id',db.Integer,db.ForeignKey('user.id'),primary_key=True),
        db.Column('disability_id',db.Integer,db.ForeignKey('disability.id'),primary_key=True)
        )
class Disability(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    disName = db.Column(db.String(100000),unique=True)


#Class User
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    mobileNum = db.Column(db.String(8))
    nric = db.Column(db.String(9))
    addr = db.Column(db.String(150))
    notes = db.relationship('Note')
    disabilities = db.relationship('Disability',secondary=ailments,backref = db.backref("ailments", lazy = 'dynamic'))
    role_id = db.Column(db.Integer,db.ForeignKey("role.id"))
    
#Class Notes
class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
#Roles
class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    roleName=db.Column(db.Integer,unique=True)
    users = db.relationship("User")


#Medical Hist
