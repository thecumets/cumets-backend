from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True

# Database details
SQLALCHEMY_DATABASE_URI = 'postgresql://cumets:cumets@localhost:5432/cumets'
