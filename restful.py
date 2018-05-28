import json
import os

import requests
from flask import Flask, request
from flask_restful import Api
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from json_raw_string_parser import get_json_obj_list
from sqlalchemy_model import db
from api_definition import ItemidsApi, PropertiesApi, CoordinateApi, NewRecordApi, SessionsApi, RegistrationApi, \
    LoginApi, UserDeleteApi, PropertiesRangeApi


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:123456@localhost/test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ALLOWED_EXTENSIONS'] = ['json']
    app.config['UPLOAD_FOLDER'] = '/static/'
    app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()


# ------------------ Upload File ------------------------#
def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', method=['GET', 'POST'])
def uploadFile():
    file = request.files['data_file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        except RequestEntityTooLarge:
            return 'File size exceed max limit (32MB)'
        with open('/static/' + filename, 'rb') as f:
            json_list = get_json_obj_list(f.read)
            for item in json_list:
                requests.post('http://localhost:5000/api/newrecord/', data=json.dumps(item))


# ----------------- API registration ----------------------#

api = Api(app)
api.add_resource(NewRecordApi, '/api/newrecord/')
api.add_resource(ItemidsApi, '/api/itemid/<string:_id>')
api.add_resource(PropertiesApi, '/api/properties/<int:id>')
api.add_resource(PropertiesRangeApi, '/api/properties')
api.add_resource(CoordinateApi, '/api/coordinate/<int:id>')
api.add_resource(RegistrationApi, '/api/register')
api.add_resource(LoginApi, '/api/login')
api.add_resource(UserDeleteApi, '/api/user/delete/<string:username>')
api.add_resource(SessionsApi, '/api/sessions/<string:token>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
