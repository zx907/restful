from geoalchemy2 import Geometry
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(32), nullable=False)
    properties = db.relationship('Properties', backref='user')
    coordinates = db.relationship('Coordinate', backref='user')

class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_tbl_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _text = db.Column(db.Text)
    userID = db.Column(db.String(32))
    userName = db.Column(db.String(32))
    _timestamp = db.Column(db.TIMESTAMP, nullable=False)
    source = db.Column(db.String(32))
    labelledSentiment = db.Column(db.String(32))
    crowder = db.Column(db.String(32))

class Coordinate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_tbl_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    coordinate = db.Column(Geometry(geometry_type='POINT'))

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.TEXT, nullable=False)
    users_tbl_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


print("in model.py")