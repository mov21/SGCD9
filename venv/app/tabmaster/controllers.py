# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for
import operator
# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.debater.models import Debater
from app.judge.models import Judge
from app.mod_auth.models import User
from app.tabmaster.models import Game, Team, Club

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc,or_

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

tabmaster = Blueprint('tabmaster', __name__, url_prefix='' , template_folder='templates')

def update_team_number_of_games(team):
    #games = Game.query.filter(or_(Game.winner == 'ed', Game.loser == 'wendy'))
    wins = games.count()
    team.wins = wins
def update_team_wins(team):
    games = Game.query.filter_by(winner=team.id)
    wins = games.count()
    team.wins = wins

def update_team_defeats(team):
    games = Game.query.filter_by(loser=team.id)
    defeats = games.count() 
    team.defeats = defeats

def update_team_points(team):
    points = 0
    oppositions = Game.query.filter_by(opposition_id=team.id)
    points += opposition_points(oppositions)
    goverments = Game.query.filter_by(goverment_id=team.id)
    points += goverment_points(goverments)
    team.points = points

def update_teams():
    teams = Team.query.all()
    for team in teams:
        update_team_points(team)
        update_team_wins(team)
        update_team_defeats(team)

def opposition_points(games):
    points = 0
    for game in games:
        
        points += game.opposition1_points
        points += game.opposition2_points
        points += game.opposition3_points
        points += game.opposition4_points
    return points
def goverment_points(games):
    points = 0
    for game in games:
        print "gov 1 " + str(game.goverment1_points)
        points += game.goverment1_points
        points += game.goverment2_points
        points += game.goverment3_points
        points += game.goverment4_points
    return points



def create_user(email,role):
    parola = id_generator()
    msg = Message(
            'Saint George City of Debate - your password',
        sender='mywusic@gmail.com',
        recipients= 
            [email])
    msg.body = "This is your password "+parola+" try it!"
    mail.send(msg)
    user = User(email,parola,role)
    print user.id
    db.session.add(user)
    db.session.commit()

def create_team(name):
    team = Team(name)
    db.session.add(team)
    db.session.commit()

def create_club(name):
    #print "create club "+name
    club = Club(name)
    #print club.name
    db.session.add(club)
    db.session.commit()

#
#
#   Tabmaster debaters
#
#
def debater_info(debaters):
    _debaters = []
    
    for debater in debaters:
        
        _debater = {}
        
        user = User.query.get(debater.user_id)
        team = Team.query.get(debater.team_id)
        club = Club.query.get(team.club_id)

        _debater['id'] = debater.id
        _debater['name'] = debater.name
        _debater['email'] = user.email
        _debater['team'] = team.name
        _debater['club'] = club.name
        _debaters.append(_debater)
    return _debaters

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
                    if not request.form['club']:
                        flash('Club is required', 'error')
                    else:

                        name = request.form['name']
                        email = request.form['email']
                        team = request.form['team']
                        club = request.form['club']
                        
                        debater = Debater(name)
                        
                        if User.query.filter_by(email = email).count() == 0:
                            create_user(email,"debater")
                        user = User.query.filter_by(email = email).one()
                        debater.user_id = user.id
                        
                        if Team.query.filter_by(name = team).count() == 0:
                            create_team(team)
                        team = Team.query.filter_by(name = team).one()   
                        debater.team_id = team.id
                        
                        if Club.query.filter_by(name = club).count() == 0:
                            create_club(club)
                        club = Club.query.filter_by(name = club).one()
                        team.club_id = club.id
                        
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
    club = Club.query.get(team.club_id)
    
    if request.method == 'GET':
        
        #
        #   GET
        #

        _debater = {}
        _debater['id'] = debater.id
        _debater['name'] = debater.name
        _debater['email'] = user.email
        _debater['team'] = team.name
        _debater['club'] = club.name
        return render_template('tabmaster/update_debater.html',debater = _debater)

    #
    #   POST
    #

    name = request.form['name']
    email = request.form['email']
    team_name = request.form['team']
    club_name = request.form['club']
    
    debater.name = name
    if(user.email != email):
        try:
            user.email = email
        except:
            flash('A different user has this email', 'error')
            return render_template('update_debater.html',debater = _debater)
    if(team.name != team_name):
        club_id = team.club_id
        create_team(team_name)
        team = Team.query.filter_by(name = team_name).one()
        debater.team_id = team.id
        team.club_id = club_id
    if(club.name != club_name):
        create_club(club_name)
        club = Club.query.filter_by(name = club_name).one()
        team.club_id = club.id    
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
    flash(name +'was successfully deleted.')
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
        club = Club.query.get(judge.club_id)
        _judge['id'] = judge.id
        _judge['name'] = judge.name
        _judge['email'] = user.email
        _judge['club'] = club.name
        _judges.append(_judge)

    return render_template('tabmaster/judges.html',judges=_judges)

#
#   CREATE
#

@tabmaster.route('/judges/create', methods=['POST', 'GET'])
@login_required
def create_judge():
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
                if not request.form['club']:
                    flash('Club is required', 'error')
                else:
                    name = request.form['name']
                    email = request.form['email']
                    club = request.form['club']
                    
                    judge = Judge(name)
                        
                    if User.query.filter_by(email = email).count() == 0:
                        create_user(email,"judge")
                    user = User.query.filter_by(email = email).one()
                    judge.user_id = user.id
                           
                    if Club.query.filter_by(name = club).count() == 0:
                        create_club(club)
                    club = Club.query.filter_by(name = club).one()
                    judge.club_id = club.id
                        
                    db.session.add(judge)
                    db.session.commit()
                    flash(judge.name + ' was successfully created')
                    return redirect(url_for('tabmaster.judges'))
    #
    #   GET
    #
    return render_template('tabmaster/create_judge.html')

#
#   Update
#

@tabmaster.route('/judges/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_judge(id):
    judge = Judge.query.get(id)
    user = User.query.get(judge.user_id)
    club = Club.query.get(judge.club_id)
    if request.method == 'GET':
        
        #
        #   GET
        #

        _judge = {}
        _judge['id'] = judge.id
        _judge['name'] = judge.name
        _judge['email'] = user.email
        _judge['club'] = club.name
        return render_template('update_judge.html', judge = _judge)

    #
    #   POST
    #

    name = request.form['name']
    email = request.form['email']
    club_name = request.form['club']
    
    debater.name = name
    
    if(user.email != email):
        try:
            user.email = email
        except:
            flash('A different user has this email', 'error')
            return render_template('update_debater.html',debater = _debater)
    if(club.name != club_name):
        create_club(club)
        club = Club.query.filter_by(name = club).one()
        judge.club_id = club.id
        
    db.session.commit()
    flash(debater.name+' was successfully updated')
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

#
#
#
#   Tabmaster Create Round
#
#
def game_info_team(team_id):
    team = Team.query.get(team_id)
    debaters = Debater.query.filter_by(team_id = team_id)
    _team = {}
    _team['name'] = team.name
    k = 1
    for debater in debaters:
        debater_string = "debater" + str(k)
        _debater = {}
        _debater['id'] = debater.id
        _debater['name'] = debater.name
        _team[debater_string] = _debater
        k = k + 1
    return _team
        

def game_info(games):
    _games = []
    for game in games:
        _game = {}
        _game['id'] = game.id
        print game.goverment_id
        print game.opposition_id
        goverment = game_info_team(game.goverment_id)
        opposition =  game_info_team(game.opposition_id)
        _game['goverment'] = goverment
        _game['opposition'] = opposition
        _game['room'] = game.room
        judge = Judge.query.get(game.judge_id)
        _game['judge'] = judge.name
        if game.has_not_decision():
            _game['has_not_decision'] = True
        else:
            _game['winner'] = Team.query.get(game.winner).name
        print _game['judge']
        _games.append(_game)
    return _games

@tabmaster.route('/round/', methods=['GET','POST'])
def round():
    if request.method == 'POST':
         return render_template("round.html")
    games = Game.query.order_by(desc(Game.round_number))
    round_number = games.first().round_number 
    games = Game.query.filter_by(round_number = round_number)
    _games = game_info(games)
    return render_template("tabmaster/round.html", games = _games, round_number = round_number)




@tabmaster.route('/create_round/', methods=['GET','POST'])
def create_round_pannel():
    return render_template("tabmaster/create_round.html")



def High_Low(teams, round_number):
    odd = False
    if len(teams) % 2 == 1:
        odd = True
    games = [] 
    i = 0 
    for team in teams:
        if odd and i == n:
            break;
        if i < n/2: 
            game = Game(round_number,i)
            game.goverment_id = team.id
            games.append(game)
        else:
            games[i-n/2].opposition_id = team.id
        i += 1
    return games

def High_High(teams, round_number):

    odd = False
    if len(teams) % 2 == 1:
        odd = True
    games = [] 
    i = 0 
    for team in teams:
        if odd and i == n:
            break;
        if i % 2 == 0: 
            game = Game(round_number,i)
            game.goverment_id = team.id
            print "gov id "+str(team.id)
            games.append(game)
        else:
            print "op id "+str(team.id)
            game.opposition_id = team.id
        i += 1
    return games

def Hidh_Low_and_Brackets(teams, round_number):
    odd = False
    if (teams.count() % 2 == 1):
        odd = True
    games = [] 
    i = 0 
    return games    

@tabmaster.route('/create_round/<mod>', methods=['GET'])
def create_round(mod):
    print "intra"
    update_teams()
    teams = Team.query.all()
    games = Game.query.all()
    if len(games) == 0:
        round_number = 0 
    else:
        games = Game.query.order_by(Game.round_number.desc())
        round_number = games.first().round_number + 1 
    
    if mod == "High_Low":
        games = High_Low(teams, round_number)
    if mod == "High_High":
         games = High_High(teams, round_number)
    
    i = 1
    for game in games:
        print "game room "+str(game.room)
        judge = Judge.query.get(i)
        game.judge_id = judge.id
        i += 1
        db.session.add(game)
    db.session.commit()
    return redirect(url_for('tabmaster.round')) 

@tabmaster.route('/clasament', methods=['GET','POST'])
def ranking():
    update_teams()
    teams = Team.query.all()
    teams.sort(key = lambda l: (l.wins, l.points),reverse = True)
    for team in teams:
        print team
    return render_template("tabmaster/ranking_teams.html",teams=teams)

@tabmaster.route('/break', methods=['GET','POST'])
def Break():
    update_teams()
    teams = Team.query.order_by(desc(Team.points)).limit(8)
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
        
        game.debaters(goverment1_id, goverment2_id, goverment3_id,\
            opposition1_id, opposition2_id, opposition3_id)\
        
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
