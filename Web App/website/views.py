#Standard Routes for Website i.e. sites without authentication

from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import  login_required, current_user
from .models import Disability, Note
from . import db
import json

views = Blueprint('views',__name__)
##Routes

#Home
@views.route('/home')
@login_required
def home():
    return render_template("home.html",user = current_user)

#Notes
@views.route('/notes',methods = ['GET','POST'])
@login_required
def note():
    if request.method=='POST':
        note = request.form.get('note')
        
        if len(note) < 1:
            flash("Note is too short",category ='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note Added!',category='success')
    return render_template("notes.html",user = current_user)

@views.route('/about')
def about():
    return render_template("about.html", user = current_user)

#Delete Note
@views.route('/delete-note',methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})

#Disability
@views.route('/med-hist',methods = ['GET','POST'])
@login_required
def disability():
    if request.method=='POST':
        dis = request.form.get('disability')
        
        if len(dis) < 1:
            flash("Enter a valid input",category ='error')
        else:
            new_dis = Disability(disName = dis, disUser_id = current_user.id)
            db.session.add(new_dis)
            db.session.commit()
            flash('Input updated!',category='success')
    return render_template("med_hist.html",user = current_user)

#Delete disability
@views.route('/delete-disability',methods=['POST'])
def delete_dis():
    dis = json.loads(request.disName)
    disId = dis['disId']
    dis = Disability.query.get(disId)
    if dis:
        if dis.disUser_id == current_user.id:
            db.session.delete(dis)
            db.session.commit()
    
    return jsonify({})