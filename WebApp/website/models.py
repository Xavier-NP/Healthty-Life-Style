from datetime import date
from typing import Sequence

from sqlalchemy import PrimaryKeyConstraint
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
    
#Class Notes
class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(100000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    
#Class User
class User(db.Model,UserMixin):
    __tablename__ ="user"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
    falls = db.relationship('Fall')
    type = db.Column('type',db.String(50))
    CalsBMIs = db.relationship('CalsBMI')
    __mapper_args__ = {'polymorphic_on':type}


    def fullName(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_diabetic(self): #Check if User is Diabetic
        if self.type != "patient":
            return False
        else:
            #diabetic = ailments.select().where(ailments.c.user_id==self.id)
            diabetic = db.session.query(ailments).filter(ailments.c.user_id==self.id ,ailments.c.disability_id==1).first()
            if diabetic:
                return True
            else:
                return False
            
    @property
    def crutched(self): #Check if User is Diabetic
        if self.type != "patient":
            return False
        else:
            #diabetic = ailments.select().where(ailments.c.user_id==self.id)
            crutched = db.session.query(ailments).filter(ailments.c.user_id==self.id ,ailments.c.disability_id==2).first()
            if crutched:
                return True
            else:
                return False
    
#Class Patient
class Patient(User):
    __tablename__="patient"
    #id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    patient_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    __mapper_args__={'polymorphic_identity':'patient',
                     'inherit_condition':(patient_id==User.id)}
    mobileNum = db.Column(db.String(8))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    nric = db.Column(db.String(9))
    addr = db.Column(db.String(150))
    disabilities = db.relationship('Disability',secondary=ailments,backref = db.backref("ailments", lazy = 'dynamic'))
    doctor_id = db.Column(db.Integer,db.ForeignKey('doctor.doctor_id'))
    
    def dName(self):
        doctor=Doctor.query.filter_by(doctor_id=self.doctor_id).first()
        return f"{doctor.full_name}"
    
    def dEmail(self):
        doctor=Doctor.query.filter_by(doctor_id=self.doctor_id).first()
        return f"{doctor.email}"
    
#Class Doctor
class Doctor(User):
    __tablename__="doctor"
    #id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    doctor_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True,autoincrement='ignore_fk')
    __mapper_args__={'polymorphic_identity':'doctor',
                     'inherit_condition':(doctor_id==User.id)}
    full_name=db.Column(db.String(50))
    patients= db.relationship("Patient",primaryjoin="(Doctor.doctor_id==Patient.doctor_id)",backref=db.backref(("doctor")))
    

#Class to store calories and BMI data
class CalsBMI(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    calories = db.Column(db.Float(10))
    bmi = db.Column(db.Float(4))
    CalsBMIdate = db.Column(db.Date())
    CalsBMIid = db.Column(db.Integer,db.ForeignKey('user.id'))

#Class for Fall Data

class Fall(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    data = db.Column(db.String(100000))
    when = db.Column(db.String(100000),default=str(func.now()))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def add_data(self):
        self.data = f"Fell down on {str(self.when)}"
    


