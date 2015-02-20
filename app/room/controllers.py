# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.room.models import Room

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
# Define the blueprint: 'admin', set its url prefix: app.url/admin
room = Blueprint('room', __name__, url_prefix='/room' , template_folder='templates')

@room.before_request
def before_request():
    if current_user is not None and current_user.is_authenticated():
        if (current_user.user_type != 'tabmaster'):
            flash('Nu sunteti admin','error')
            return redirect(url_for('home'))
    else:
        flash('You must log in to continue','error')
        return redirect(url_for('auth.login'))


@room.route('/')
@login_required
def rooms():
    rooms =Room.query.order_by(Room.name)
    _rooms = []
    for room in rooms:
        _room = {}
        _room['id'] = room.id
        _room['name'] = room.name
        _room['area'] = room.area
        _rooms.append(_room)
    ##return "mazare"
    return render_template('room/rooms.html', rooms = _rooms)    


@room.route('/create/', methods=['POST', 'GET'])
@login_required
def create_room():
    if request.method == 'GET':
        
        #
    	#   GET
    	#
    	return render_template('room/create_room.html')
    #
    #   POST
    #
    if not request.form['name']:
        flash('Name is required', 'error')
        return render_template('room/create_room.html')
    else:
        if not request.form['area']:
            flash('Email is required', 'error')
            return render_template('room/create_room.html')
        else:
            name = request.form['name']
            area = request.form['area']
                
            room = Room(name, area)
                        
            db.session.add(room)
            db.session.commit()
            flash(room.name + ' was successfully created')
        return redirect(url_for('room.rooms'))
    
#
#   Delete
#


@room.route('/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_room(id):
    print id
    if request.method == 'GET':
            print id
            room = Room.query.get(id)
            print room.name
            print room.area
            db.session.delete(room)
            db.session.commit()
            flash(room.name + ' was successfully deleted.')
    return redirect(url_for('room.rooms'))


#
#   Update
#

@room.route('/update/<id>', methods=['POST', 'GET'])
@login_required
def update_room(id):
    room = Room.query.get(id)
    if request.method == 'GET':
        
        #
        #   GET
        #

        _room = {}
        _room['id'] = room.id
        _room['name'] = room.name
        _room['area'] = room.area
        return render_template('room/update_room.html', room = _room)

    #
    #   POST
    #

    name = request.form['name']
    area = request.form['area']
    
    room.name = name
    room.area = area

    db.session.commit()
    flash(room.name+' was successfully updated')
    return redirect(url_for('room.rooms'))

