# Import flask and template operators
from flask import Flask, render_template
# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Import Flask-Login
from flask.ext.login import current_user

#from app.mod_auth.controllers import login as login

# Define the WSGI application object
app = Flask(__name__)

#login_manager.blueprint_login_views = 'auth.login'
# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.admin.controllers import admin as admin_module
from app.tabmaster.controllers import tabmaster as tabmaster_module
from app.judge.controllers import judge as judge_module
from app.debater.controllers import debater as debater_module
from app.room.controllers import room as room_module

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(admin_module)
app.register_blueprint(tabmaster_module)
app.register_blueprint(judge_module)
app.register_blueprint(debater_module)
app.register_blueprint(room_module)
# ..
# ..

from flask.ext.mail import Mail, Message

from app.mod_auth.controllers import mail
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)
app.config.update(
    DEBUG = True,
    # Flask-Mail Configuration
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'mywusic@gmail.com',
    MAIL_PASSWORD = 'pr2j1tur1c2',
    DEFAULT_MAIL_SENDER = 'mywusic@gmail.com'
    )
mail.init_app(app)
@app.route('/')
def home():
	return render_template('home.html')


@app.before_request
def before_request():
    g.user = current_user
# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

