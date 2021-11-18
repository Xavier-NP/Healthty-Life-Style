# from datetime import datetime
# from . import db
# from .models import Note
# from flask_restful import Api,Resource,reqparse,fields,marshal_with


# #Mobile Diary
# diary_post_args = reqparse.RequestParser()
# diary_post_args.add_argument("data",type=str,help="Content of the Note!",required=True)
# diary_post_args.add_argument("user_id",type=int,help="User id",required=True)

# resource_fields = {
#     'id':fields.Integer,
#     'user_id':fields.Integer,
#     'data':fields.String
# }
# class Diary(Resource):
#     @marshal_with(resource_fields)
#     def get(self,note_id):
#         result = Note.query.get(user_id=note_id)
#         return result
    
#     @marshal_with(resource_fields)
#     def post(self,note_id):
#         args = diary_post_args.parse_args()
#         note = Note(id=note_id,data=args['data'],user_id=args['user_id'])
#         db.session.add(note)   
#         db.session.commit()
#         return note,201
         
# api.add_resource(Diary,"/api/<int:note_id>")


            
#Crutches
