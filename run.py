import os
import configparser

from app import create_app

config = configparser.ConfigParser()
config.read('.env')

config_var = ''

if 'FLASK_ENV' in os.environ:
   config_var = os.getenv('FLASK_ENV')
else:
   config_var = config['DEFAULT']['FLASK_ENV']

app = create_app(config_var)