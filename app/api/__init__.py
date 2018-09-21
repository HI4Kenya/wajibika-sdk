import requests
from flask import Blueprint

BASE_URL = "https://play.dhis2.org/demo/api/26"

AUTH = ('admin', 'district')


class AuthMissingError(Exception):
   pass

if AUTH is None:
   raise AuthMissingError(
      "All methods require a username and password"
   )

session = requests.Session()
session.auth = AUTH

api = Blueprint('api', __name__, url_prefix='/api')

from . import views