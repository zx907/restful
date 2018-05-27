from datetime import datetime

from flask import request, json
from flask.json import jsonify
from flask_restful import Resource

from json_raw_string_parser import get_json_obj_list
from sqlalchemy_model import db, User, Properties, Coordinate

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
class UserApi(Resource):
    def get(self, _id):
        """GET method to return data about user id and _id"""
        user = User.query.filter_by(_id=_id).first()
        if user is None:
            return 1
        return jsonify(user.to_dict())

    def put(self, _id):
        """PUT method to update user table with json format payload"""
        user = User.query.filter_by(_id=_id).first()
        req_data_dict = json.loads(request.data)
        print(req_data_dict)
        for k, v in req_data_dict.items():
            setattr(user, k, v)
        return jsonify(user.to_dict())

    def delete(self, _id):
        """DELETE method to remove one record from user table
        Since user table has cascade deletion attr, delete one record from user table
        will also remove related record from properties table and coordinate table.
        """
        try:
            user = User.query.filter_by(_id=_id).first()
            db.session.delete(user)
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


