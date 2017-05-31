from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mongoengine import MongoEngine
from flask_wtf import CSRFProtect
from config import Config

# Init flask packages
bootstrap = Bootstrap()
csrf = CSRFProtect()
moment = Moment()
db = MongoEngine()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config['SECRET_KEY']

    bootstrap.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
