from app import db

class Judge(db.Model):
	__tablename__= "judges"
	id = db.Column('judge_id', db.Integer, primary_key=True)
	name = db.Column(db.String(30))
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	club_id = db.Column(db.Integer, db.ForeignKey('clubs.club_id'))

	def __init__(self, name):
		self.name = name