from os import path
from os import environ

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True

# Database details
#SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
SQLALCHEMY_DATABASE_URI = 'postgresql://cumets:cumets@10.212.64.22:5432/cumets'
