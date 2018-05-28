from datetime import datetime
from functools import wraps

from flask import request, json
from flask.json import jsonify
from flask_restful import Resource

from json_raw_string_parser import get_json_obj_list
from sqlalchemy_model import db, Itemids, Properties, Coordinate, Users, Sessions

from itsdangerous import TimestampSigner, SignatureExpired, BadSignature, URLSafeTimedSerializer
import requests

SECRET_KEY = "demo"  # secret key for token


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        if token is None:
            return "Missing token"
        s = URLSafeTimedSerializer(SECRET_KEY)
        try:
            s.loads(token, max_age=60 * 10)
            session_token = Sessions.query.filter_by(token=token).first()
            if session_token:
                return func(*args, **kwargs)
        except SignatureExpired:
            requests.delete('http://localhost:5000/api/sessions/' + token)
            return "token expired"
        except BadSignature:
            return 'Invalid token'

    return wrapper


# Add a raw json list text data (from test.json) to database
class NewRecordApi(Resource):

    def post(self):
        json_obj_list = get_json_obj_list(request.data)

        try:
            for json_obj in json_obj_list:
                _timestamp = datetime(int(json_obj['properties']['year']),
                                      int(json_obj['properties']['month']),
                                      int(json_obj['properties']['day']),
                                      int(json_obj['properties']['hour']),
                                      int(json_obj['properties']['minute']),
                                      int(json_obj['properties']['second']))

                properties = Properties(_text=json_obj['properties']['text'],
                                        userID=json_obj['properties']['userID'],
                                        userName=json_obj['properties']['userName'],
                                        _timestamp=_timestamp,
                                        source=json_obj['properties']['source'],
                                        sentiment=json_obj['properties']['sentiment'],
                                        sentiStrings=json_obj['properties']['sentiStrings'],
                                        labelledSentiment=json_obj['properties']['labelledSentiment'],
                                        crowder=json_obj['properties']['crowder'])

                coordinate = Coordinate(latitude=float(json_obj['coordinate']['coordinates'][0]),
                                        longtitude=float(json_obj['coordinate']['coordinates'][1]))

                item_id = Itemids(_id=json_obj['_id'], properties=properties, coordinates=coordinate)

                db.session.add(item_id)
                db.session.add(properties)
                db.session.add(coordinate)
                db.session.commit()

                return "Post successfully"

        except Exception as e:
            print(e)
            db.session.rollback()
            return "Failed to post"
        finally:
            db.session.close()


# Query user table with _id (or id?)
class ItemidsApi(Resource):
    @token_required
    def get(self, _id):
        """GET method to return data about user id"""
        item_ids = Itemids.query.filter_by(_id=_id).first()
        if item_ids is None:
            return "Record not found\n, Did you send in an index instead of _id"
        return jsonify(item_ids.to_dict())

    @token_required
    def put(self, _id):
        """PUT method to update user table with json format payload"""
        item_ids = Itemids.query.filter_by(_id=_id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(item_ids, k, v)
        return jsonify(item_ids.to_dict())

    @token_required
    def delete(self, _id):
        """DELETE method to remove one record from user table
        Since user table has cascade deletion attr, delete one record from user table
        will also remove related record from properties table and coordinate table.
        """
        try:
            item_ids = Itemids.query.filter_by(_id=_id).first()
            db.session.delete(item_ids)
            db.session.commit()
            return 0
        except:
            db.session.rollback()
            return 1
        finally:
            db.session.close()


class PropertiesApi(Resource):
    @token_required
    def get(self, id):
        properties = Properties.query.filter_by(id=id).first()
        if properties is None:
            return 1
        return jsonify(properties.to_dict())

    @token_required
    def put(self, id):
        properties = Properties.query.filter_by(id=id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(properties, k, v)
        return jsonify(properties.to_dict())

    @token_required
    def delete(self, id):
        try:
            properties = Properties.query.filter_by(id=id).first()
            db.session.delete(properties)
            db.session.commit()
            return 0
        except:
            db.session.rollback()
            return 1
        finally:
            db.session.close()


# Demo for fetch ranged data
class PropertiesRangeApi(Resource):
    def get(self):
        offset, limit = request.args.get('offset'), request.args.get('limit')
        properties = Properties.query.order_by(Properties.id.asc()).limit(limit).offset(offset).all()
        string = ""
        for p in properties:
            s = json.dumps(p.to_dict())
            string += s
        return string


class CoordinateApi(Resource):
    @token_required
    def get(self, id):
        coordinate = Coordinate.query.filter_by(id=id).first()
        if coordinate is None:
            return 1
        return jsonify(coordinate.to_dict())

    @token_required
    def put(self, id):
        coordinate = Coordinate.query.filter_by(id=id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(coordinate, k, v)
        return jsonify(coordinate.to_dict())

    @token_required
    def delete(self, id):
        try:
            coordinate = Coordinate.query.filter_by(id=id).first()
            db.session.delete(coordinate)
            db.session.commit()
            return 0
        except:
            db.session.rollback()
            return 1
        finally:
            db.session.close()


# User registration api,
class RegistrationApi(Resource):
    # Assume that user send in registration request with json format e.g.{"username":"uname", "password":"pwd"}
    def post(self):
        try:
            data = json.loads(request.data)
            if Users.query.filter_by(username=data['username']).first():
                return "This username is used, change to another one to continue"
            user = Users(username=data['username'])
            user.hash_password(data['password'])
            db.session.add(user)
            db.session.commit()
            return "Register successfully"
        except Exception as e:
            db.session.rollback()
            print(e)
            return "registration failed"
        finally:
            db.session.close()


class LoginApi(Resource):
    def get(self):  # args: username and password
        user = Users.query.filter_by(username=request.args.get('username')).first()

        if user and user.verify_password(request.args.get('password')):
            s = URLSafeTimedSerializer(SECRET_KEY)
            token = s.dumps(str(user.id))
            print(token)

            try:
                user_session = Sessions(token=token)
                # add logged in user to session table
                db.session.add(user_session)
                db.session.commit()
                return token
            except Exception as e:
                db.session.rollback()
                return e
            finally:
                db.session.close()
        else:
            return "Cannot find this user info"


class UserDeleteApi(Resource):
    # Delete account
    @token_required
    def delete(self, username):
        try:
            user = Users.query().filter_by(username=username).first()
            db.session.delete(user)
            db.commit()
            return "Delete successfully"
        except:
            db.session.rollback()
            return "Failed to delete this account"
        finally:
            db.close()


class SessionsApi(Resource):
    def get(self, token):
        session_token = Sessions.query.filter_by(token=token).first()
        if session_token:
            try:
                s = URLSafeTimedSerializer(SECRET_KEY)
                s.loads(token, max_age=60 * 10)
                return 0
            except SignatureExpired:
                requests.delete('http://localhost:5000/api/sessions/' + token)
                return "token expired"
            except BadSignature:
                return 'Invalid token'
        else:
            return "cannot find matching token"  # cannot find the token

    # New session record is automaticaaly inserted when User GET method returns true,
    # so no POST method is defined here
    @token_required
    def delete(self, token):
        session_id = Sessions.query.filter_by(token=token).first()
        if session_id:
            try:
                db.session.delete(session_id)
                db.commit()
                return "Delete successfully"
            except:
                db.session.rollback()
                return "Failed to remove this session"
            finally:
                db.close()
        else:
            return "Cannot find this token"
