# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import password / encryption helper tools
from werkzeug import check_password_hash, generate_password_hash

# Import the database object from the main app module
from app import db

# Import module models (i.e. User)
from app.mod_auth.models import User
from app.judge.models import Judge
from app.tabmaster.models import Game
# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Flask-Login
from flask.ext.login import login_user , logout_user , current_user , login_required


from datetime import datetime
from flask import Flask,session, request, flash, url_for, redirect, render_template, abort ,g,request

from app.tabmaster.controllers import game_info
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
# Define the blueprint: 'admin', set its url prefix: app.url/admin
judge = Blueprint('judge', __name__, url_prefix='/' , template_folder='templates')


@judge.route('/program')
@login_required
def program():
    return render_template('judge/program.html')

@judge.route('/games')
@login_required
def judge_games():
    judge = Judge.query.filter_by(user_id = current_user.id).one()
    games = Game.query.filter_by(judge_id = judge.id)
    _games = game_info(games)
    return render_template('judge/judge_games.html', games = _games)

@judge.route('/games/decision/<int:id>',methods=['POST','GET'])
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
        return redirect(url_for('judge.judge_games'))

    games = []
    games.append(game)
    _games = game_info(games)
    _game = _games.pop()
    return render_template('judge/game_decision.html', game = _game)

@judge.route('/about')
@login_required
def about_sfantu_gheorghe():
    return render_template('judge/about_sfantu_gheorghe.html') 