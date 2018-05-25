from flask import Flask
from model import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:123456@localhost/test2'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)