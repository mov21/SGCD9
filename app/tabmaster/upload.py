from app import db

# Import csv 
import csv

# Import Debater class
from app.mod_auth.models import User
from app.debater.models import Debater
from app.tabmaster.models import Team, Game
from app.judge.models import Judge
from app.tabmaster.functions import create_user, create_team, create_judge, update_round_number


def upload_debaters(filename):
    with open(filename, 'rb') as f:
    	reader = csv.reader(f)
  			
  	for row in reader:
   		print row
   		print row[1]

   		create_team(row[0])
   		team = Team.query.filter_by(name = row[0]).first()

   		for i in [1,3,5]:
   			debater = Debater(row[i])
   			create_user(row[i+1],"debater")
   			user = User.query.filter_by(email = row[i+1]).one()
   			debater.user_id = user.id
			debater.team_id = team.id

			db.session.add(debater)
			db.session.commit()


def upload_judges(filename):
    with open(filename, 'rb') as f:
    	reader = csv.reader(f)
  			
  	for row in reader:
   		
   		judge = Judge(row[0])
   		create_judge(row[1])

   		user = User.query.filter_by(email = row[1]).one()
   		judge.user_id = user.id

		db.session.add(judge)
		db.session.commit()

runde =0
def upload_rounds(filename):
  f = open(filename, 'rb')
  for row in f:
    print row
    [room, team1, team2, judge] = row.split(",")

    print room
    print team1
    print team2
    print judge
    
    round_number = runde
    game = Game(round_number,room)
    print game.room
    government = Team.query.filter_by(name = team1).one()
    opposition = Team.query.filter_by(name = team2).one()
    #_judge = Judge.query.filter_by(name = judge).first()
    judges = Judge.query.all()
    _judges = []
    for judge in judges:
      user = User.query.get(judge.user_id)
      print user.email


    game.government_id = government.id
    game.opposition_id = opposition.id
    game.judge_id = _judge.id

    db.session.add(game)
    db.session.commit()

    g = Game.query.filter_by(room = room).first()
    p = Game.query.filter_by(room = room)
    print p
    print g.room
    print g.round_number




def read_from_cvs(filename):
    with open(filename, 'rb') as f:
    	reader = csv.reader(f)
  			
  	for row in reader:
   		print row
	