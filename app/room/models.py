from app import db

class Room(db.Model):
	__tablename__ = "rooms"
	id = db.Column('room_id', db.Integer , primary_key=True)
	name = db.Column(db.String(30))
	area = db.Column(db.String(30)) 
	#games = db.relationship('Game', backref='game', lazy='dynamic')
	def __init__(self, name, area):
		self.name = name 
		self.area = area
