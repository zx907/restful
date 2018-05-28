from flask import Flask
from flask_restful import Api

from sqlalchemy_model import db
from api_definition import ItemidsApi, PropertiesApi, CoordinateApi, NewRecordApi, SessionsApi, RegistrationApi, \
    LoginApi, UserDeleteApi, PropertiesRangeApi


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:123456@localhost/test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()

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
