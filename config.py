from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True

# Database details
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
