from flask import Flask
from redis import Redis

# from flask_bootstrap import Bootstrap
# from flask_mail import Mail
# from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
from config import config

# bootstrap = Bootstrap()
# mail = Mail()
# moment = Moment()
# db = SQLAlchemy()
redis_db = Redis(host='redis', port=6379)


# def create_app(config_name):
def create_app():
    app = Flask(__name__)


    # app.config.from_object(config[config_name])
    # config[config_name].init_app(app)

    # bootstrap.init_app(app)
    # mail.init_app(app)
    # moment.init_app(app)
    # db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

