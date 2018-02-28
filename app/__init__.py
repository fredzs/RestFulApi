"""request api"""


from flask import Flask

from app.api.Entity.Config import Config
from app.api.Factory.ConfigFactory import ConfigFactory
from config import config


CONFIG = ConfigFactory.read_config("config.txt")


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app
