from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class ItemIds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _id = db.Column(db.String(32), nullable=False)
    properties = db.relationship('Properties', uselist=False, backref='user')
    coordinates = db.relationship('Coordinate', uselist=False, backref='user', cascade="delete")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Properties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemids_tbl_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    _text = db.Column(db.Text)
    userID = db.Column(db.String(32))
    userName = db.Column(db.String(32))
    _timestamp = db.Column(db.TIMESTAMP, nullable=False)
    source = db.Column(db.String(32))
    sentiment = db.Column(db.String(32))
    sentiStrings = db.Column(db.Text)
    labelledSentiment = db.Column(db.String(32))
    crowder = db.Column(db.String(32))

    def to_dict(self):
        ret_val = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret_val.pop('itemids_tbl_id')
        return ret_val


class Coordinate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemids_tbl_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float)
    longtitude = db.Column(db.Float)

    def to_dict(self):
        ret_val = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        ret_val.pop('users_tbl_id')
        return ret_val


class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.TEXT, nullable=False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        check_password_hash(self.password_hash, password)
