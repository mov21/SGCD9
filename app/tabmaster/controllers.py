# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
import operator
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db
from app.mod_auth.controllers import mail
# Import module models (i.e. User)
from app.debater.models import Debater
from app.judge.models import Judge,Debater_restriction,Team_restriction
from app.mod_auth.models import User
from app.tabmaster.models import Game, Team
from app.tabmaster.upload import upload_judges, upload_debaters, upload_rounds
from functions import *

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Import Secure filename for file uploading
import os
from werkzeug import secure_filename
from flask import send_from_directory

# Import csv 
import csv

ALLOWED_EXTENSIONS = set(['txt', 'xml', 'csv'])

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print APP_ROOT
(APP_ROOT, f) = os.path.split(APP_ROOT)
print APP_ROOT
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
print UPLOAD_FOLDER
#UPLOAD_FOLDER = '/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from flask.ext.mail import Mail, Message

from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc,or_


tabmaster = Blueprint('tabmaster', __name__, url_prefix='' , template_folder='templates')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@tabmaster.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file_type = request.form['result']
        print file_type
        if file and allowed_file(file.filename):
            flash('File Successfully Uploaded')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            path_filename = os.path.join(UPLOAD_FOLDER, filename)

            if file_type == 'debater':
                print "da"
                upload_debaters(path_filename)
                #TODO
            if file_type == 'arbitru':
                upload_judges(path_filename)
                #TODO
            if file_type == 'runde':
                upload_rounds(path_filename)
                #TODO
    return render_template('tabmaster/upload_file.html')

@tabmaster.before_request
def before_request():
    if current_user is not None and current_user.is_authenticated():
        if (current_user.user_type != 'tabmaster'):
            flash('Nu sunteti tabmaster!','error')
            return redirect(url_for('home'))
    else:
        flash('You must log in to continue','error')
        return redirect(url_for('auth.login'))


# TODO
@tabmaster.route('/game_decisions', methods=['POST', 'GET'])
@login_required
def game_decisions():
    print decision


@tabmaster.route('/uploads', methods=['POST', 'GET'])
@login_required
def uploads():
    print "upload functie"
    return redirect(url_for('upload_file'))

@tabmaster.route('/debaters', methods=['GET'])
@login_required
def debaters():
    debaters = Debater.query.all()
    _debaters = debater_info(debaters)
    return render_template('tabmaster/debaters.html',debaters=_debaters)

#
#   CREATE
#

@tabmaster.route('/debaters/create', methods=['POST', 'GET'])
@login_required
def create_debater():

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
                if not request.form['team']:
                    flash('Team is required', 'error')
                else:

                    name = request.form['name']
                    email = request.form['email']
                    team = request.form['team']
                        
                    debater = Debater(name)
                        
                    if User.query.filter_by(email = email).count() == 0:
                        create_user(email,"debater")
                    user = User.query.filter_by(email = email).one()
                    debater.user_id = user.id
                        
                    if Team.query.filter_by(name = team).count() == 0:
                        create_team(team)
                    team = Team.query.filter_by(name = team).one()   
                    debater.team_id = team.id
                        
                    db.session.add(debater)
                    db.session.commit()
                    flash(debater.name + ' was successfully created')
                    return redirect(url_for('tabmaster.debaters'))
    
    #
    #   GET
    #

    return render_template('tabmaster/create_debater.html')

#
#   UPDATE
#

@tabmaster.route('/debaters/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_debater(id):

    debater = Debater.query.get(id)
    user = User.query.get(debater.user_id)
    team = Team.query.get(debater.team_id)

    if request.method == 'GET':
        
        #
        #   GET
        #

        _debater = {}
        _debater['id'] = debater.id
        _debater['name'] = debater.name
        _debater['email'] = user.email
        _debater['team'] = team.name
        return render_template('tabmaster/update_debater.html',debater = _debater)

    #
    #   POST
    #

    name = request.form['name']
    email = request.form['email']
    team_name = request.form['team']
    
    debater.name = name
    if(user.email != email):
        try:
            user.email = email
        except:
            flash('A different user has this email', 'error')
            return render_template('update_debater.html',debater = _debater)
    if(team.name != team_name):
        create_team(team_name)
        team = Team.query.filter_by(name = team_name).one()
        debater.team_id = team.id  
    db.session.commit()
    flash(debater.name+' was successfully updated')
    return redirect(url_for('tabmaster.debaters'))

#
#   DELETE
#

@tabmaster.route('/debaters/delete/<id>', methods=['GET'])
def delete_debater(id):
    debater = Debater.query.get(id)
    name = debater.name
    db.session.delete(debater)
    db.session.commit()
    flash(name +' was successfully deleted.')
    return redirect(url_for('tabmaster.debaters'))




#
#
#   Tabmaster judges
#
#

@tabmaster.route('/judges', methods=['GET'])
@login_required
def judges():
    judges = Judge.query.all()
    _judges = []
    for judge in judges:
        _judge = {}
        user = User.query.get(judge.user_id)
        
        _judge = judge_info(judge, user.email)
        _judges.append(_judge)

    return render_template('tabmaster/judges.html',judges=_judges)

#
#   CREATE
#


@tabmaster.route('/judges/create', methods=['POST', 'GET'])
@login_required
def create_judge():
    
    if request.method == 'GET':
        #
        #   GET
        #
        return render_template('tabmaster/create_judge.html')

    #
    #   POST
    #
    if not request.form['category']:
            flash('Categorie is required', 'error')
    else:    
        if not request.form['name']:
            flash('Name is required', 'error')
        else:
            if not request.form['email']:
                flash('Email is required', 'error')
            else:
                category = request.form['category']
                name = request.form['name']
                email = request.form['email']
                
                judge = Judge(name,category)
                    

                if User.query.filter_by(email = email).count() == 0:
                    create_user(email,"judge")
                user = User.query.filter_by(email = email).one()
                judge.user_id = user.id

                    

                db.session.add(judge)
                db.session.commit()
                if request.form['teams_restriction']:
                    print "team res"
                    teams_restriction = request.form['teams_restriction']
                    update_teams_restriction(teams_restriction,judge.id)
                if request.form['debaters_restriction']:
                    print "debater res"
                    debaters_restriction = request.form['debaters_restriction']
                    update_debaters_restriction(debaters_restriction,judge.id)

                    
                    flash(judge.name + ' was successfully created')
                    return redirect(url_for('tabmaster.judges'))
    
#
#   Update
#


@tabmaster.route('/judges/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_judge(id):
    judge = Judge.query.get(id)
    user = User.query.get(judge.user_id)
    if request.method == 'GET':
        
        #
        #   GET
        #
        _judge = judge_info(judge, user.email)
        delete_restrictions(judge.id)
        return render_template('tabmaster/update_judge.html', judge = _judge)

    #
    #   POST
    #

    name = request.form['name']
    email = request.form['email']
    category = request.form['category']              

    judge.name = name
    
    if(user.email != email):
        try:
            user.email = email
        except:
            flash('A different user has this email', 'error')
            return render_template('update_debater.html',debater = _debater)
    
    judge.category = category

    if request.form['teams_restriction']:
        print "team res"
        teams_restriction = request.form['teams_restriction']
        update_teams_restriction(teams_restriction,judge.id)
    if request.form['debaters_restriction']:
        print "debater res"
        debaters_restriction = request.form['debaters_restriction']
        update_debaters_restriction(debaters_restriction,judge.id)

    db.session.commit()
    flash(judge.name+' was successfully updated')
    return redirect(url_for('tabmaster.judges'))

#
#   DELETE
#

@tabmaster.route('/judges/delete/<id>', methods=['GET'])
def delete_judge(id):
    judge = Judge.query.get(id)
    name = judge.name
    db.session.delete(judge)
    db.session.commit()
    flash(name +'was successfully deleted.')
    return redirect(url_for('tabmaster.judges'))

@tabmaster.route('/judges/available/<id>', methods=['GET'])
def judge_available(id):
    judge = Judge.query.get(id)
    judge.available = True
    db.session.commit()
    flash('Judge ' + judge.name +' is available.')
    return redirect(url_for('tabmaster.judges'))

@tabmaster.route('/judges/not_available/<id>', methods=['GET'])
def judge_not_available(id):
    judge = Judge.query.get(id)
    judge.available = False
    db.session.commit()
    flash('Judge ' + judge.name +' is not available.')
    return redirect(url_for('tabmaster.judges'))

#
#
#
#   Tabmaster Create Round
#
#

@tabmaster.route('/round/', methods=['GET','POST'])
def round():
    if request.method == 'POST':
        return render_template("round.html")
    #games = Game.query.all()
    #round_number = get_round_number()
    round_number = 1
    #games = Game.query.order_by(desc(Game.round_number))
    
    #print "round number " + str(round_number) 
    games = Game.query.all()

   # _games = game_info(games)
    return render_template("tabmaster/round.html", games = games, round_number = round_number)

@tabmaster.route('/echipe', methods=['GET','POST'])
def teams():
    teams = Team.query.all()
    _teams = []
    for team in teams:
        _teams.append(team_info(team.id))
    return render_template("tabmaster/teams.html", teams = _teams)

@tabmaster.route('/create_round/', methods=['GET','POST'])
def create_round():
    
    #print request.form['password']
    if request.method == 'GET':
        return render_template("tabmaster/create_round.html",email=current_user.email)
    if not round_finished():
        flash("Trebuie sa se incheie runda actuala ")
        return redirect(url_for('tabmaster.round'))
    
    pairing_altgotihm = request.form['pairing_altgotihm']
    print pairing_altgotihm
    round_type = request.form['round_type']
    password = request.form['password']
    
    if not current_user.check_password(password):
        flash('Invalid password', 'error')
        return render_template("tabmaster/create_round.html",email=current_user.email)
    
    update_teams()
        
    games = pairing_altgotihms(pairing_altgotihm);
    if len(games) == 0:
        return render_template("tabmaster/create_round.html",email=current_user.email)    
    
    judge_number = 0
    update_restriction_points()
    
    
    judge_to_games(games)

    return redirect(url_for('tabmaster.round')) 

@tabmaster.route('/clasament', methods=['GET','POST'])
def ranking():
    update_teams()
    teams = Team.query.all()
    team = Team.query.filter_by(name='None')
    print team
    #teams.remove(team)
    teams.sort(key = lambda l: (l.wins, l.points),reverse = True)
    return render_template("tabmaster/ranking_teams.html",teams=teams)

@tabmaster.route('/break', methods=['GET','POST'])
def Break():
    update_teams()
    teams = Team.query.all()
    teams.sort(key = lambda l: (l.wins, l.number_of_games , l.points),reverse = True)
    teams = teams[0:7]
    return render_template("tabmaster/ranking_teams.html",teams=teams)

@tabmaster.route('/upload', methods=['GET','POST'])
def upload():
    return render_template("tabmaster/ranking_teams.html")

@tabmaster.route('/round/decision/<int:id>',methods=['POST','GET'])
@login_required
def decision(id):
    game = Game.query.get(id)
    if request.method == 'POST':
        print "post" 
        winner = request.form['winner']
        print winner
        decision_motivation = request.form['decision_motivation']
        
        goverment1_id = request.form['goverment1_id']
        goverment2_id = request.form['goverment2_id']
        goverment3_id = request.form['goverment3_id']
        goverment4_id = request.form['goverment4_id']
        

        goverment1_points = request.form['goverment1_points']
        goverment2_points = request.form['goverment2_points']
        goverment3_points = request.form['goverment3_points']
        goverment4_points = request.form['goverment4_points']
        

        opposition1_id = request.form['opposition1_id']
        opposition2_id = request.form['opposition2_id']
        opposition3_id = request.form['opposition3_id']
        opposition4_id = request.form['opposition4_id']
        
        opposition1_points = request.form['opposition1_points']
        opposition2_points = request.form['opposition2_points']
        opposition3_points = request.form['opposition3_points']
        opposition4_points = request.form['opposition4_points']
        
        game.goverment_debaters(goverment1_id, goverment2_id, goverment3_id)
        game.opposition_debaters(opposition1_id, opposition2_id, opposition3_id)
        
        if winner == "goverment":
            game.decision(game.goverment_id, game.opposition_id, goverment1_points,\
                goverment2_points, goverment3_points, goverment4_points, opposition1_points,\
                opposition2_points,opposition3_points, opposition4_points, decision_motivation)
        else:
            if winner == "opposition":
                game.decision(game.opposition_id, game.goverment_id, goverment1_points,\
                    goverment2_points, goverment3_points, goverment4_points, opposition1_points,\
                    opposition2_points,opposition3_points, opposition4_points, decision_motivation)
        db.session.commit()
        return redirect(url_for('tabmaster.round'))

    games = []
    games.append(game)
    _games = game_info(games)
    _game = _games.pop()
    return render_template('tabmaster/game_decision.html', game = _game)


@tabmaster.route('/game_select_modify_judge/<id>', methods=['GET','POST'])
def game_select_modify_judge(id):
    game = Game.query.get(id)
    judges = Judge.query.all()
    _judges = []
    for judge in judges:
        if Game.query.filter_by(judge_id = judge.id, round_number = game.round_number).count() == 0:
            if verify_restriction(game,judge):
                user = User.query.get(judge.user_id)
                _judges.append(judge_info(judge,user.email))
    return render_template("tabmaster/game_select_modify_judge.html",judges = _judges,game_id = id)

@tabmaster.route('/game_modify_judge/<game_id>/<judge_id>', methods=['GET'])
def game_modify_judge(game_id,judge_id):
    game = Game.query.get(game_id)
    judge = Judge.query.get(judge_id)
    if verify_restriction(game,judge):
        game.judge_id = judge_id
        db.session.commit()
        return redirect(url_for('tabmaster.round'))    
    return redirect(url_for('tabmaster.game_select_modify_judge',id = game_id))
