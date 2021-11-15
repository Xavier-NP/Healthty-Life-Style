from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    contact = db.Column(db.String(8), primary_key=True)
    email = db.Column(db.String(150), unique=True)
    icnumber = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(150))
    fName = db.Column(db.String(150))
    def get_id(self):
        return (self.contact)
