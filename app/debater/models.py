from app import db

class Debater(db.Model):
	__tablename__ = "debaters"
	id = db.Column('debater_id', db.Integer , primary_key=True)
	name = db.Column(db.String(30)) 
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
	debater_res = db.relationship('Debater_restriction', backref='debater_res', lazy='dynamic')
	def __init__(self, name):
		self.name = name 
