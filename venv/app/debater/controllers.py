# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.mod_auth.models import User
from app.debater.models import Debater
from app.tabmaster.models import Game

from app.tabmaster.controllers import game_info
from app.tabmaster.controllers import debater_info
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
# Define the blueprint: 'admin', set its url prefix: app.url/admin
debater = Blueprint('debater', __name__, url_prefix='' , template_folder='templates')

@debater.route('/program')
@login_required
def program():
    return render_template('debater/program.html')

@debater.route('/meciuri')
@login_required
def debater_games():
	if Debater.query.filter_by(user_id = current_user.id).count() == 1:
		debater = Debater.query.filter_by(user_id = current_user.id).one()
		games = []
		games.extend(Game.query.filter_by(opposition_id = debater.team_id))
    	games.extend(Game.query.filter_by(goverment_id = debater.team_id))
    	_games = game_info(games)
    	return render_template('debater/debater_games.html', games = _games)

@debater.route('/echipa')
@login_required
def team():
    debater = Debater.query.filter_by(user_id = current_user.id).one()
    debaters = Debater.query.filter_by(team_id = debater.team_id).filter(Debater.user_id != debater.id)
    _debaters = debater_info(debaters)
		#team = Team.query.filter_by(team_id = debater.team_id)
    return render_template('debater/team.html', debaters = _debaters)


@debater.route('/about')
@login_required
def about_sfantu_gheorghe():
    return render_template('debater/about_sfantu_gheorghe.html') 