# global imports
from flask import Flask
# Add more here ...


# local imports
from config import app_config
# Add more here ...


def create_app(config_var):
   app = Flask(__name__, instance_relative_config=True)
   app.config.from_object(app_config[config_var])
   app.config.from_pyfile('config.py')

   # Add blueprints here
   from .api import api as api_blueprint
   app.register_blueprint(api_blueprint)

   return app
