from . import db
from .models import Notes
from ..main import api 
from flask_restful import Api,Resource,reqparse
from flask import request
test ={}

#Mobile Diary
dairy_post_args = reqparse.RequestParser()
dairy_post_args.add_argument("")
class Diary(Resource):
    def get(self,diary_id):
        return test[diary_id]
    def post(self,diary_id):
        return   
         
api.add_resource(Diary,"/dairy/<diary_id>")


            
#Crutches
