from website import create_app
from website import db
from website.models import Note,User
from flask_restful import Api,Resource,reqparse,fields,marshal_with
from sqlalchemy import func
#!!!!!!!!!!! Before Deploying,change to .website !!!!!!!!!!! 
app = create_app()


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
    def get(self,note_id):
        result = Note.query.filter_by(id=note_id).first()
        return result
    
    @marshal_with(diary_resource_fields)
    def post(self,note_id):
        args = diary_post_args.parse_args()
        ph = Note.query.get(note_id)
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

#User API

user_resource_fields = {
    'id':fields.Integer,
    'email':fields.String,
    'password':fields.String
}

class UserApi(Resource):
    @marshal_with(user_resource_fields)
    def get(self,user_email):
        result = User.query.filter_by(email=user_email).first()
        return result

api.add_resource(UserApi,"/api/user/<user_email>")



if __name__ == '__main__':
    app.run(debug=1)