from flask import request
from flask_restful import Resource, request
from restful import User

class UsersApi(Resource):
    def get(self):
        user = User.query()
        return
