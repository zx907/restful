from flask import Flask
from flask_restful import Api, Resource, reqparse
import secrets  # require python 3.6
from jsparse import json_obj

app = Flask(__name__)
api = Api(app)


class SR(Resource):
    def get(self, id):
        return json_obj

    def put(self, id):
        pass

    def delete(self, id):
        pass



api.add_resource(SR, '/api/v0.1/<int:id>')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)