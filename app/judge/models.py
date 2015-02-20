from app import db

class Judge(db.Model):
    __tablename__= "judges"
    id = db.Column('judge_id', db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.club_id'))
    debater_restrictions = db.relationship('Debater_restriction', backref='debater_restriction', lazy='dynamic')
    team_restrictions = db.relationship('Team_restriction', backref='team_restriction', lazy='dynamic') 
    club_restrictions = db.relationship('Club_restriction', backref='club_restriction', lazy='dynamic') 
    category = db.Column(db.Integer)
    restriction_points = db.Column(db.Integer)
    available = db.Column(db.Boolean)
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.available = True
        self.restriction_points = 0

class Debater_restriction(db.Model):
    __tablename__ = "debater_restrictions"
    id = db.Column('debater_restriction_id', db.Integer, primary_key=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('judges.judge_id'))
    debater_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    restriction_name = db.Column(db.String(30))
    def __init__(self, restriction_name, judge_id, debater_id = None):
        self.restriction_name = restriction_name
        self.judge_id = judge_id
        self.debater_id = debater_id
        

class Team_restriction(db.Model):
    __tablename__ = "team_restrictions"
    id = db.Column('team_restriction_id', db.Integer, primary_key=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('judges.judge_id'))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    restriction_name = db.Column(db.String(30))
    def __init__(self, restriction_name, judge_id, team_id = None):
        self.restriction_name = restriction_name
        self.judge_id = judge_id
        self.team_id = team_id
        

class Club_restriction(db.Model):
    __tablename__ = "club_restrictions"
    id = db.Column('club_restriction_id', db.Integer, primary_key=True)
    judge_id = db.Column(db.Integer, db.ForeignKey('judges.judge_id'))
    club_id = db.Column(db.Integer, db.ForeignKey('clubs.club_id'))
    restriction_name = db.Column(db.String(30))
    def __init__(self, restriction_name, judge_id, club_id = None):
        self.restriction_name = restriction_name
        self.judge_id = judge_id
        self.club_id = club_id