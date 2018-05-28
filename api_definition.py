from datetime import datetime

from flask import request, json
from flask.json import jsonify
from flask_restful import Resource

from json_raw_string_parser import get_json_obj_list
from sqlalchemy_model import db, ItemIds, Properties, Coordinate, Users, Sessions

from werkzeug.security import generate_password_hash, check_password_hash
import secrets

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

                user = User(_id=json_obj['_id'], properties=properties, coordinates=coordinate)

                db.session.add(user)
                db.session.add(properties)
                db.session.add(coordinate)
                db.session.commit()

                return 0

        except Exception as e:
            print(e)
            db.session.rollback()
            return 1
        finally:
            db.session.close()

# Query user table with _id (or id?)
class ItemIdsApi(Resource):
    def get(self, _id):
        """GET method to return data about user id and _id"""
        item_ids = ItemIds.query.filter_by(_id=_id).first()
        if item_ids is None:
            return 1
        return jsonify(item_ids.to_dict())

    def put(self, _id):
        """PUT method to update user table with json format payload"""
        item_ids = ItemIds.query.filter_by(_id=_id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(item_ids, k, v)
        return jsonify(item_ids.to_dict())

    def delete(self, _id):
        """DELETE method to remove one record from user table
        Since user table has cascade deletion attr, delete one record from user table
        will also remove related record from properties table and coordinate table.
        """
        try:
            item_ids = ItemIds.query.filter_by(_id=_id).first()
            db.session.delete(item_ids)
            db.session.commit()
            return 0
        except:
            db.session.rollback()
            return 1
        finally:
            db.session.close()


class PropertiesApi(Resource):
    def get(self, id):
        properties = Properties.query.filter_by(id=id).first()
        if properties is None:
            return 1
        return jsonify(properties.to_dict())

    def put(self, id):
        properties = Properties.query.filter_by(id=id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(properties, k, v)
        return jsonify(properties.to_dict())

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


class CoordinateApi(Resource):
    def get(self, id):
        coordinate = Coordinate.query.filter_by(id=id).first()
        if coordinate is None:
            return 1
        return jsonify(coordinate.to_dict())

    def put(self, id):
        coordinate = Coordinate.query.filter_by(id=id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(coordinate, k, v)
        return jsonify(coordinate.to_dict())

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


class UserApi(Resource):
    def get(self, username, pwd):
        user = Users.query.filter(username=username).first()
        if user and user.verify_password(pwd):
            token = secrets. toekn_hex(32)
            try:
                user_session = Sessions(token=token)
                db.session.add(user_session)
                return secrets.toekn_hex(32)
            except Exception as e:
                db.session.rollback()
                return e
            finally:
                db.session.close()
        else:
            return "Cannot find this user info"

    # Assume that user send in registration request with json format e.g.{"username":"uname", "password":"pwd"}
    def post(self):
        try:
            data = json.loads(request.data)['username']
            user = Users(username=data['username'])
            user.password_hash = user.hash_password(data['password'])
            db.session.add(user)
            db.session.commit()
            return "Register successfully"
        except Exception as e:
            db.session.rollback()
            print(e)
            return "registration failed"
        finally:
            db.session.close()