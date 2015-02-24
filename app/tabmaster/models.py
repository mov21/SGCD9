from app import db

class Team(db.Model):
    __tablename__ = "teams"
    id = db.Column('team_id', db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    points = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    defeats = db.Column(db.Integer)
    number_of_games = db.Column(db.Integer)
    #
    #oras si liceu 
    #
    team_res = db.relationship('Team_restriction', backref='team_res', lazy='dynamic') 
    debaters = db.relationship('Debater', backref='team', lazy='dynamic')

    def __init__(self, name):
        self.name = name
        self.points = 0
        self.wins = 0
        self.defeats = 0
        self.number_of_games = 0

    def __repr__(self):
        return '{}:wins {} defeats {} points {}'.format(self.name,
                                  self.wins,
                                  self.defeats,
                                  self.points)


class Game(db.Model):
    __tablename__= "games"
    id = db.Column('game_id', db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    goverment_id= db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    opposition_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    round_number = db.Column(db.Integer)
    room = db.Column(db.String(30))
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
    winner = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    loser = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    decision_motivation = db.Column(db.String(300))
    judge_id = db.Column(db.Integer, db.ForeignKey('judges.judge_id'))
    goverment1_points = db.Column(db.Integer)
    goverment1_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    goverment2_points = db.Column(db.Integer)
    goverment2_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    goverment3_points = db.Column(db.Integer)
    goverment3_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    goverment4_points = db.Column(db.Integer)
    opposition1_points = db.Column(db.Integer)
    opposition1_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    opposition2_points = db.Column(db.Integer)
    opposition2_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    opposition3_points = db.Column(db.Integer)
    opposition3_id = db.Column(db.Integer, db.ForeignKey('debaters.debater_id'))
    opposition4_points = db.Column(db.Integer)
    time = db.Column(db.DateTime)
    private = db.Column(db.Boolean)
    #
    #   Judge feedback !?
    #
    def __init__(self, round_number, room):
        self.round_number = round_number
        self.room = room
        self.goverment1_points = 0
        self.goverment2_points = 0
        self.goverment3_points = 0
        self.goverment4_points = 0
        self.opposition1_points = 0
        self.opposition2_points = 0
        self.opposition3_points = 0
        self.opposition4_points = 0

    def goverment_debaters(self,gov1,gov2,gov3):
        self.goverment1_id = gov1
        self.goverment2_id = gov2
        self.goverment3_id = gov3
    
    def opposition_debaters(self,opp1,opp2,opp3):
        self.opposition1_id = opp1
        self.opposition2_id = opp2
        self.opposition3_id = opp3

    def decision(self,winner,loser,gov1,gov2,gov3,gov4,opp1,opp2,opp3,opp4,decision_motivation):
        self.winner = winner
        self.loser = loser

        self.decision_motivation = decision_motivation


    def has_not_decision(self):
        if self.winner is not None:
            return False
        else:
            return True
