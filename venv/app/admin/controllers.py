# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.mod_auth.models import User
from app.admin.models import Tabmaster

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

# Flask-Mail
from flask.ext.mail import Mail ,Message
app = Flask(__name__)
mail=Mail(app)
app.config.from_object(__name__)
app.config.update(
    DEBUG=True,
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'mywusic',
    MAIL_PASSWORD = 'pr2j1tur1c2',
    DEFAULT_MAIL_SENDER = 'mywusic@gmail.com'
    )
mail=Mail(app)

# Password Generator
import string
import random
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



# Define the blueprint: 'admin', set its url prefix: app.url/admin
admin = Blueprint('admin', __name__, url_prefix='' , template_folder='templates')

def create_user(email,role):
    parola = id_generator()
    msg = Message(
            'Saint George City of Debate - your password',
        sender='mywusic@gmail.com',
        recipients= 
            [email])
    msg.body = "You are a tabmaster. This is your password "+parola+" try it!"
    mail.send(msg)
    user = User(email,parola,role)
    print user.id
    db.session.add(user)
    db.session.commit()


@admin.route('/admin/tabmasters/create', methods=['POST', 'GET'])
@login_required
def create_tabmaster():
    if request.method == 'POST':
        #
        #   POST
        #
        if not request.form['name']:
            flash('Name is required', 'error')
        else:
            if not request.form['email']:
                flash('Email is required', 'error')
            else:
                name = request.form['name']
                email = request.form['email']
                
                tabmaster = Tabmaster(name)
                    
                if User.query.filter_by(email = email).count() == 0:
                    create_user(email,"tabmaster")
                user = User.query.filter_by(email = email).one()
                tabmaster.user_id = user.id
                        
                db.session.add(tabmaster)
                db.session.commit()
                flash(tabmaster.name + ' was successfully created')
                return redirect(url_for('admin.tabmasters'))
    #
    #   GET
    #
    return render_template('admin/create_tabmaster.html')

#
#   Delete
#


@admin.route('/tabmasters/delete/<id>', methods=['POST', 'GET'])
@login_required
def delete_tabmaster(id):
    print id
    if request.method == 'GET':
            print id
            _tabmaster = Tabmaster.query.get(id)
            db.session.delete(_tabmaster)
            db.session.commit()
            flash('Tab Master Successfully deleted.')
    return redirect(url_for('admin.tabmasters'))


#
#   Update
#

@admin.route('/tabmasters/update/<id>', methods=['POST', 'GET'])
@login_required
def update_tabmaster(id):
    tabmaster = Tabmaster.query.get(id)
    prev_tabmaster_name = tabmaster.name
    user = User.query.get(tabmaster.user_id)
    if request.method == 'GET':
        
        #
        #   GET
        #

        _tabmaster = {}
        _tabmaster['id'] = tabmaster.id
        _tabmaster['name'] = tabmaster.name
        _tabmaster['email'] = user.email
        return render_template('admin/update_tabmaster.html', tabmaster = _tabmaster)

    #
    #   POST
    #

    name = request.form['name']
    email = request.form['email']
    
    tabmaster.name = name
    tabmaster.mail = email
    
    if(user.email != email):
        try:
            user.email = email
        except:
            flash('A different user has this email', 'error')
            return render_template('admin/update_tabmaster.html',tabmaster = _tabmaster)
        
    db.session.commit()
    flash(prev_tabmaster_name+' was successfully updated')
    return redirect(url_for('admin.tabmasters'))


@admin.route('/tabmasters/')
@login_required
def tabmasters():
    tabmasters =Tabmaster.query.all()
    _tabmasters = []
    for tabmaster in tabmasters:
        _tabmaster = {}
        _tabmaster['id'] = tabmaster.id
        _tabmaster['name'] = tabmaster.name
        user = User.query.get(tabmaster.user_id)
        _tabmaster['email'] = user.email
        _tabmasters.append(_tabmaster)
    ##return "mazare"
    return render_template('admin/tabmasters.html', tabmasters = _tabmasters)    
