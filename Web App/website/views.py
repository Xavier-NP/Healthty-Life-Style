from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
#from .models import 
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/')#returns to the home page if no page chosen
def homeAlso():
    return render_template("home.html")

@views.route('/about')
def about():
    return render_template("about.html")

