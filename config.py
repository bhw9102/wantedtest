import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_KEy = '816307c8243548874e7a17487da3e72a3af503e1739a37d9'

USERNAME = 'coding'
PASSWORD = '1233'

DATABASE_NAME = 'wantedtest'
SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@localhost:5432/{2}'.format(USERNAME, PASSWORD, DATABASE_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True

HOST = '0.0.0.0'
PORT = 5000


