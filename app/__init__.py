from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import CSRFProtect
from redis import Redis

bootstrap = Bootstrap()
csrf = CSRFProtect()
moment = Moment()

redis_db = Redis(host='redis', port=6379)

secret_key = '\xa9<#I\xce\x93\x0c\x86\xa3R\xf9\xb3\xc3\x9f\xf1q%\xcb]M\xb0\xb4~\xc7'

# from flask_mail import Mail
# from flask_sqlalchemy import SQLAlchemy
from config import config

# mail = Mail()
# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key

    bootstrap.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)

    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)


    # mail.init_app(app)

    # db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
