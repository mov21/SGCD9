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
from functions import *

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from flask.ext.mail import Mail, Message

from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc,or_
# Password Generator
import string
import random



#
#
#
#
#

def team_info(team_id):
    team = Team.query.get(team_id)
    debaters = Debater.query.filter_by(team_id = team_id)
    _team = {}
    _team['id'] = team.id
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
        print game.winner
        print game.has_not_decision()
        _game = {}
        _game['id'] = game.id
        print game.goverment_id
        print "bunica"
        print game.opposition_id
        goverment = team_info(game.goverment_id)
        _game['goverment'] = goverment
        
        if game.opposition_id is not None:
            opposition =  team_info(game.opposition_id)
            _game['opposition'] = opposition
            #game['opposition'] = "None"
        _game['room'] = game.room
        if game.judge_id is not None:
            judge = Judge.query.get(game.judge_id)
            _game['judge'] = judge.name
        if game.has_not_decision():
            _game['has_not_decision'] = True
        else:
            _game['winner'] = Team.query.get(game.winner).name
        _games.append(_game)
    return _games


#
#
#
#
#

def sort(teams):
    teams.sort(key = lambda l: (l.wins, l.number_of_games , l.points),reverse = True)
    return teams

def none_team():
    teams = Team.query.filter_by(name="None")
    if teams.count() == 0:
        team = Team("None")
        db.session.add(team)
        db.session.commit()
    else:
        team = teams.first()
    return team        

def High_Low(teams, round_number, odd, number_teams):
    games = []
    print "n= "+ str(number_teams) 
    i = 1 
    for team in teams:
        print team.name
        print "i= " + str(i)
        sala_number = i / 2 + 1 
        if odd and i == number_teams:
            game = Game(round_number,sala_number)
            game.goverment_id = team.id
            #games.opposition_id = none_team.id
            game.winner = team.id
            #game.loser = none_team.id
            print "n impar"
            print "gov " + str(team.id)
            print "team id " + str(team.id)
            print "game winner " + str(game.winner) 
            games.append(game)
            break;
        
        if  number_teams/2 >= i: 
            game = Game(round_number,sala_number)
            game.goverment_id = team.id
            print "gov " + str(team.id)
            games.append(game)
            k = i/2 
        else: 
            position = (number_teams - i)/2 #-n/2-1
            print "position = " + str(position)
            games[k].opposition_id = team.id
            print "opp " + str(team.id)
            k -= 1
        
        #1   1-6 i = 6 n = 6
        #2   2-5 i = 5 n = 6
        #3   3-4 i = 4 n = 6
        # 

        i += 1
    return games

def High_High(teams, round_number, odd, number_teams):
    print "da High high"
    games = [] 
    i = 1 
    print "n= "+ str(number_teams)
    for team in teams:
        print "i= " + str(i)
        sala_number = i / 2 +1
        if odd and i == number_teams:
            game = Game(round_number,sala_number)
            print "team id " + str(team.id)
            game.goverment_id = team.id
            #games.opposition_id = none_team.id
            game.winner = team.id
            print "game winner " + str(game.winner)
            #game.loser = none_team.id
            games.append(game) 
            break
        if i % 2 == 1: 
            game = Game(round_number,sala_number)
            game.goverment_id = team.id
            print "gov id "+str(team.id)
            games.append(game)
        else:
            print "op id "+str(team.id)
            game.opposition_id = team.id
        i += 1
    return games

def High_Low_and_Brackets(teams, round_number, odd, number_teams):
    games = [] 
    i = 0 
    return games    

def update_round_number():
    games = Game.query.all()
    if len(games) == 0:
        round_number = 1 
    else:
        games = Game.query.order_by(Game.round_number.desc())
        round_number = games.first().round_number + 1
    return round_number

def get_round_number():
    games = Game.query.all()
    if len(games) == 0:
        round_number = 0
    else:
        games = Game.query.order_by(Game.round_number.desc())
        round_number = games.first().round_number
    return round_number

def pairing_altgotihms(pairing_altgotihm):
    
    round_number = update_round_number()
    print "round number " + str(round_number)
    teams = Team.query.all()
    number_teams = len(teams)
    

    judges = Judge.query.all();
    if number_teams/2 > len(judges):
        print "arbitrii"
        flash('Too low number of judges', 'error')
        return []
    odd = False
    
    if number_teams % 2 == 1:
        odd = True
    print "odd = " + str(odd)
    
    if pairing_altgotihm == "High_Low":
        games = High_Low(teams, round_number, odd, number_teams)
    if pairing_altgotihm == "High_High":
        games = High_High(teams, round_number, odd, number_teams)
    return games


#
#
#
#
#


def update_teams_restriction(teams_restriction,judge_id):
    teams_name = teams_restriction.split(",")
    for team_name in teams_name:
        teams = Team.query.filter_by(name = team_name)
        if teams.count() > 0:
            team = teams.one()
            restrinction = Team_restriction(team_name,judge_id,team.id)
        else:  
            restrinction = Team_restriction(team_name,judge_id)
        print restrinction.restriction_name
        print restrinction.judge_id
        db.session.add(restrinction)
    db.session.commit()
        

def update_debaters_restriction(debaters_restriction,judge_id):
    debaters_name = debaters_restriction.split(",")
    for debater_name in debaters_name:
        debaters = Debater.query.filter_by(name = debater_name)
        if debaters.count() > 0:
            debater = debaters.one()
            restrinction = Debater_restriction(debater_name,judge_id,debater.id)
        else:  
            restrinction = Debater_restriction(debater_name,judge_id)
        print restrinction.restriction_name
        print restrinction.judge_id
        db.session.add(restrinction)
    db.session.commit()


#
#
#
#
#
def id_generator(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def update_team_number_of_games(team):
    team.number_of_games = team.wins + team.defeats

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
        update_team_number_of_games(team)

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
    user = User(email,"123abc",role)
    db.session.add(user)
    db.session.commit()

def create_team(name):
    team = Team(name)
    db.session.add(team)
    db.session.commit()

def create_judge(email):
    parola = id_generator()
    msg = Message(
        'Saint George City of Debate - your password',
        sender='mywusic@gmail.com',
        recipients=[email])
    msg.body = "This is your Password "+parola+" try it!"
    mail.send(msg)
    user = User(email, parola, "judge")
    db.session.add(user)
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

        _debater['id'] = debater.id
        _debater['name'] = debater.name
        _debater['email'] = user.email
        _debater['team'] = team.name
        _debaters.append(_debater)
    return _debaters



#
#
#   Judge restrictions
#
#


def restrictions_to_string(restrictions):
    restrictions_name = []
    for restriction in restrictions:
        restrictions_name.append(restriction.restriction_name)
    restrictions_string = ""
    if restrictions.count() > 0:
        restrictions_string = ",".join(restrictions_name) 
    return restrictions_string

def get_team_restrictions(judge_id):
    restrictions = Team_restriction.query.filter_by(judge_id = judge_id)
    return restrictions_to_string(restrictions)
def get_debater_restrictions(judge_id):
    restrictions = Debater_restriction.query.filter_by(judge_id = judge_id)
    return restrictions_to_string(restrictions)

def judge_info(judge, email):
    _judge = {}
    _judge['id'] = judge.id
    _judge['name'] = judge.name
    _judge['email'] = email
    _judge['category'] = judge.category
    _judge['available'] = judge.available
    _judge['teams_restriction'] = get_team_restrictions(judge.id)
    _judge['debaters_restriction'] = get_debater_restrictions(judge.id)
    return _judge

def detele_restrictions(restrictions):
    for restriction in restrictions:
        db.session.delete(restriction)
    db.session.commit()


def delete__team_restrictions(judge_id):
    restrictions = Team_restriction.query.filter_by(judge_id = judge_id)
    return detele_restrictions(restrictions)
def delete__debater_restrictions(judge_id):
    restrictions = Debater_restriction.query.filter_by(judge_id = judge_id)
    return detele_restrictions(restrictions)

def delete_restrictions(judge_id):
    delete__team_restrictions(judge_id)
    delete__debater_restrictions(judge_id)



def teams_restriction_points(judge_id):
    #print Team_restriction.query.filter_by(judge_id = judge_id).count()
    #print "team "+str(Team_restriction.query.filter_by(judge_id = judge_id).count()*3)
    return Team_restriction.query.filter_by(judge_id = judge_id).count()*3
def debaters_restriction_points(judge_id):
    #print Debater_restriction.query.filter_by(judge_id = judge_id).one().restriction_name
    #print "debater "+str(Debater_restriction.query.filter_by(judge_id = judge_id).count()*3)
    return Debater_restriction.query.filter_by(judge_id = judge_id).count()*3

def update_restriction_points():
    judges = Judge.query.all()
    for judge in judges:
        restriction_points = 0
        print "restrictii "+str(judge.id)+" "+str(restriction_points)
        restriction_points += teams_restriction_points(judge.id)
        print "restrictii "+str(judge.id)+" "+str(restriction_points)
        restriction_points += debaters_restriction_points(judge.id)
        print "restrictii "+str(judge.id)+" "+str(restriction_points)
        print "restrictii "+str(judge.id)+" "+str(restriction_points)
        judge.restriction_points = restriction_points
    db.session.commit()


def verify_restriction_teams(game, judge):
    restrictions = Team_restriction.query.filter_by(judge_id = judge.id)
    for restriction in restrictions:
        if restriction.team_id == game.goverment_id:
            return False
        if restriction.team_id == game.opposition_id:
            return False
    return True
def verify_restriction_debaters(game, judge):
    restrictions = Team_restriction.query.filter_by(judge_id = judge.id)
    for restriction in restrictions:
        if restriction.team_id == game.goverment1_id:
            return False
        if restriction.team_id == game.opposition1_id:
            return False
        if restriction.team_id == game.goverment2_id:
            return False
        if restriction.team_id == game.opposition2_id:
            return False
        if restriction.team_id == game.goverment3_id:
            return False
        if restriction.team_id == game.opposition3_id:
            return False
    return True

def verify_restriction(game, judge):
    print "verify team"
        
    print verify_restriction_teams(game, judge)
    
    if not verify_restriction_teams(game, judge):
        return False
    print verify_restriction_debaters(game, judge)
    
    if not verify_restriction_debaters(game, judge):
        return False
    return True
def judge_distribution(games, judges, contor, number_of_games):
    teams = Team.query.all()
    for judge in judges:
        print judge.name
        print judge.category
        print judge.restriction_points
        if contor == number_of_games:
            break;
        judge_has_game = False
        for game in games:
            # pentru runde cu numar de echipe impare
            if game.winner:
                db.session.add(game)
                break
            print "game judge id "+str(game.judge_id)
            if not game.judge_id:
                #print game.id
                if verify_restriction(game,judge):
                    judge_has_game = True
                    print judge.id
                    game.judge_id = judge.id
                    break;
                else:
                    print "nu a trecut de verificare"
        if judge_has_game == True:
            print "contor game judge id "+str(game.judge_id)
            db.session.add(game)
            contor += 1
    db.session.commit()
    return contor

def judge_to_games(games):
    number_of_games = len(games)
    i = 0
    
    judges_no1 = Judge.query.filter(Judge.available,Judge.category == 1 ).order_by(desc(Judge.restriction_points))
    i += judge_distribution(games, judges_no1, i, number_of_games)
    if i < number_of_games:
        judges_no2 = Judge.query.filter(Judge.available,Judge.category == 2 ).order_by(Judge.restriction_points)
        i+=judge_distribution(games, judges_no2, i, number_of_games)
    if i < number_of_games:
        judges_no3 = Judge.query.filter(Judge.available,Judge.category == 3 ).order_by(Judge.restriction_points)
        judge_distribution(games, judges_no3, i, number_of_games)
    #for judge in judges_no1

def round_finished():
    round_number = get_round_number()
    if round_number == 0:
        return True
    games = Game.query.filter_by(round_number = round_number)
    teams = Team.query.all()
    teams.sort(key = lambda l: (l.wins, l.points),reverse = True)
    finished = True
    
    for game in games:
        if game.has_not_decision():
            finished = False
    
    if finished:
        print "numar echipe " + str(len(teams))
        if len(teams) % 2 == 1:
            points = 0
            points += opposition_points(games)
            points += goverment_points(games)
            
            print "id gov"
            for game in games:
                if not game.opposition1_id:
                    _game = game
            game = _game
            print "puncte " + str(points)
            print "numar jocuri "+str(games.count())
            average = points/(7*(games.count()-1))
            print "medie " + str(average)
            print game.id
            game.goverment_points(average,average,average,average/2)
            print game.goverment_id
            print game.goverment1_points
            db.session.commit()
        return True
    return False