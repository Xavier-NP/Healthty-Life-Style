from dataclasses import field
from datetime import datetime
from tokenize import String
from .website import create_app
from .website import db
from .website.models import Note,User,Patient,User,Disability,Fall
from .website import create_app
from .website import db
from flask_restful import Api,Resource,reqparse,fields,marshal_with
from sqlalchemy import func
from flask_mail import Mail,Message
import hashlib
from flask_login import login_user, login_required, logout_user, current_user
from flask import Blueprint,request,jsonify
import json

#!!!!!!!!!!! Before Deploying,change to .website !!!!!!!!!!! 
app = create_app()

mail = Mail(app)


####################APIs for Mobile APP#############################
api = Api(app)


#Mobile Diary
diary_post_args = reqparse.RequestParser()
diary_post_args.add_argument("data",type=str,help="Content of the Note!",required=True)
diary_post_args.add_argument("user_id",type=int,help="User id",required=True)

diary_resource_fields = {
    'id':fields.Integer,
    'user_id':fields.Integer,
    'data':fields.String
}
class Diary(Resource):
    @marshal_with(diary_resource_fields)
    #### Find Note
    def get(self,note_id):
        result = Note.query.filter_by(id=note_id).first()
        return result
    
    @marshal_with(diary_resource_fields)
    ###### Add Note
    def post(self,note_id):
        args = diary_post_args.parse_args()
        ph = Note.query.get(note_id) # Check if note id exists
        if ph:
            new_id = db.session.query(func.max(Note.id)).scalar()
            note_id= new_id + 1
            note = Note(id=note_id,data=args['data'],user_id=args['user_id'])
            db.session.add(note)   
            db.session.commit()
            return note,201
        else:
            note = Note(id=note_id,data=args['data'],user_id=args['user_id'])
            db.session.add(note)   
            db.session.commit()
            return note,201
         
api.add_resource(Diary,"/api/<int:note_id>")

#Fall Logging
fall_args = reqparse.RequestParser()
fall_args.add_argument("date",type=str,help="date",required=True)
fall_args.add_argument("user_id",type=int,help="User id",required=True)

fall_resource_fields = {
    'id':fields.Integer,
    'user_id':fields.Integer,
    'date':fields.String
}
class FallBook(Resource):
    @marshal_with(fall_resource_fields)
    ###### Add Fall
    def post(self):
        args = fall_args.parse_args()
        # ph = Fall.query.get(fall_id)
        # new_id = db.session.query(func.max(Fall.id)).scalar()
        # fall_id= new_id + 1
        fall =  Fall(date=args['date'],user_id=args['user_id'])
        fall.add_data()
        db.session.add(fall)   
        db.session.commit()
        return fall,201
         
api.add_resource(FallBook,"/api/fall")

#User API

user_resource_fields = {
    'id':fields.Integer,
    'email':fields.String,
    'password':fields.String
}

class UserApi(Resource):
    @marshal_with(user_resource_fields)
    #Get User Info based on email
    def get(self,user_email):
        result = User.query.filter_by(email=user_email).first()
        return result
    
api.add_resource(UserApi,"/api/user/<user_email>")

# Patient API


patient_post_args = reqparse.RequestParser()
patient_post_args.add_argument("first_name",type=str,help="Your First Name",required=True)
patient_post_args.add_argument("last_name",type=str,help="Your Last Name",required=True)
patient_post_args.add_argument("email",type=str,help="Email",required=True)
patient_post_args.add_argument("mobileNum",type=str,help="mobileNum",required=True)
patient_post_args.add_argument("nric",type=str,help="nric",required=True)
patient_post_args.add_argument("addr",type=str,help="addr",required=True)
patient_post_args.add_argument("password1",type=str,help="password",required=True)
patient_post_args.add_argument("password2",type=str,help="password",required=True)
patient_post_args.add_argument("doctor_id",type=int,help="doctor_id",required=True)
#patient_post_args.add_argument("disabilities",type=str,action='append',help="disabilities",required=True)
patient_post_args.add_argument("disabilities1",type=str,help="disabilities1",required=True)
patient_post_args.add_argument("disabilities2",type=str,help="disabilities2",required=True)

patient_resource_fields = {
    'first_name':fields.String,
    'last_name':fields.String, 
    'email':fields.String, 
    'mobileNum':fields.String, 
    'nric':fields.String, 
    'addr':fields.String, 
    'password1':fields.String,
    'password2':fields.String,
    'doctor_id':fields.Integer,
    #'disabilities':fields.String,
    'disabilities1':fields.String,
    'disabilities2':fields.String
}

class PatientApi(Resource):
    @marshal_with(patient_resource_fields)
    def post(self,email):#To Add User as Patient
        args = patient_post_args.parse_args()
        ph = Patient.query.filter_by(email=email).first()
        if ph:
            errormsg = "User Exists"
            return errormsg,404
        elif len(args['email'])<3:
            errormsg = 'Email must be more then 3 Characters'
            return errormsg,404
        elif len(args['first_name'])<2:
            errormsg = 'First Name must be more than 1 Character'
            return errormsg,404
        elif len(args['last_name'])<2:
            errormsg = 'Last Name must be more than 1 Character'
            return errormsg,404
        elif len(args['mobileNum'])!=8:
            errormsg = 'Enter a valid 8 digit mobile number'
            return errormsg,404
        elif len(args['nric'])!=9:
            errormsg = 'Enter a valid NRIC/FIN'
            return errormsg,404
        elif len(args['password1'])<7:
            errormsg = 'Password must be at least 7 Characters'
            return errormsg,404
        elif args['password1'] != args['password2']:
            errormsg = 'Password does not match'
            return errormsg,404
        # elif (args['disabilities1']==False)&(args['disabilities2']==False):
        #     errormsg = 'Please select a disability!'
        #     return errormsg,404
            
        else:
            pw = hashlib.sha256()
            pw.update(args['password1'].encode("utf-8"))
            patient = Patient(first_name=args['first_name'],
                              last_name=args['last_name'],
                              email=args['email'],
                              mobileNum=args['mobileNum'],
                              nric=args['nric'],
                              addr=args['addr'],
                              password=pw.digest().hex(),
                              doctor_id=args['doctor_id'],
                              
                              )
            # for x in range(len(args['disabilities'])):
            #     dist_name=Disability.query.filter_by(disName=args['disabilities'][x]).first()
            #     patient.disabilities.append(dist_name)
            if args['disabilities1'] == "true":
                patient.disabilities.append(Disability.query.filter_by(disName='Diabetes').first())
            if args['disabilities2'] == "true":
                patient.disabilities.append(Disability.query.filter_by(disName='Crutches').first())
                
                
            db.session.add(patient)   
            db.session.commit()
            return patient,201
        

        
        
api.add_resource(PatientApi,"/api/register/<email>")


############## Mail Server###################
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'pleasegivemeAforpfd@gmail.com'
app.config['MAIL_PASSWORD'] = 'pleasegivemeA123'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

email = Blueprint('email',__name__)
@email.route('/mail',methods=['POST'])
def hello():
    #Get User's Doctor Email
    data = request.get_json()
    patient = Patient.query.filter_by(patient_id =data.get('user_id')).first()
    dEmail = patient.dEmail()
    msg = Message(
            'Fall Alert!',
            sender =dEmail,
            recipients = [patient.email]
            )
    msg.body = f" Patient {patient.first_name} {patient.last_name} Fell on {data.get('date')}\n Patient Number {patient.mobileNum}"
    mail.send(msg)
    
    return jsonify(data) #"Sent",201

app.register_blueprint(email, url_prefix='/')



if __name__ == '__main__':
    app.run(debug=1)