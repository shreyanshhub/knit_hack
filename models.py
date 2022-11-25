from . import db
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Scores(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    team_name = db.Column(db.String(100))
    score = db.Column(db.Integer)
