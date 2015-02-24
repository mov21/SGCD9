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


def upload_rounds(filename):
    with open(filename, 'rb') as f:
    	reader = csv.reader(f)
  			
  	for row in reader:
  		round_number = update_round_number()
   		game = Game(round_number,row[0])
   		government = Team.query.filter_by(name = row[1]).one()
   		opposition = Team.query.filter_by(name = row[2]).one()
   		judge = Judge.query.filter_by(name = row[3]).one()

   		game.government_id = government.id
   		game.opposition_id = opposition.id
   		game.judge = judge

   		list_government = Debater.query.filter_by(team_id = government.id)
   		for debater in list_government:
   			print debater.name


		db.session.add(game)
		db.session.commit()



def read_from_cvs(filename):
    with open(filename, 'rb') as f:
    	reader = csv.reader(f)
  			
  	for row in reader:
   		print row
	