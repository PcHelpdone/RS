from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import current_app
from queue import Queue
from . import queue,price

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)
    try:
        if queue:
            pass
    except:
        UnboundLocalError
        create_queue()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('instance/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("DATABASE created Succesfully!")

def create_queue():
    queue_wait = Queue(maxsize=10)
    with open('queue.py') as r:
        r.write(queue_wait)

def addtoqueue(member):
    with open("queue.py") as r:
        r.write(member)

def getcurrentprice():
    currentprice = price.price
    return currentprice