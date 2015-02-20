# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.mod_auth.models import User

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from werkzeug.security import generate_password_hash, check_password_hash


from flask.ext.login import LoginManager
 
from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.login import login_user , logout_user , current_user , login_required
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


login_manager = LoginManager()
# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='' , template_folder='templates')

@mod_auth.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('auth/register.html')
    user = User(request.form['email'],  request.form['password'], request.form['user_type'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('auth.login'))

@mod_auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Username is invalid' , 'error')
        return redirect(url_for('auth.login'))
    if not registered_user.check_password(password):
        flash('Password is invalid','error')
        return redirect(url_for('auth.login'))
    login_user(registered_user, remember = remember_me)

    if registered_user.user_type == 'admin':
        print "Admin"
        return redirect(url_for('admin.tabmasters'))
    if registered_user.user_type == 'tabmaster':
        print "Tabmaster"
        return redirect(url_for('tabmaster.debaters'))
    return redirect(url_for('debater.program'))

@mod_auth.route('/settings', methods=['GET','POST'])
def settings():
    if request.method == 'GET':
        return render_template('auth/settings.html')
    oldpassword = request.form['password']
    newpassword = request.form['newpassword']
    newpassword_verification = request.form['newpassword_verification']
    if not current_user.check_password(oldpassword):
        flash('Password is invalid','error')
        return render_template('auth/settings.html')
    if newpassword == newpassword_verification:
        current_user.set_password(newpassword)
        db.session.commit()
        msg = Message(
            'Saint George City of Debate - your password',
            sender='mywusic@gmail.com',
            recipients= 
                [current_user.email])
        msg.body = "You have changed your password. This is your new password "+newpassword+" try it!"
        mail.send(msg)
        flash('Successfully changed your password')
        return render_template('auth/settings.html')
    else:
        flash('The passwords do not match','error')
        return render_template('auth/settings.html')
    return render_template('auth/settings.html')

@mod_auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home')) 

@mod_auth.record_once
def on_load(state):
    login_manager.init_app(state.app)
    login_manager.login_view = '/auth/login'


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
