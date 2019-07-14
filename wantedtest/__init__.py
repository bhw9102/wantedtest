from flask import Flask
from flask_sqlalchemy import SQLALchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '816307c8243548874e7a17487da3e72a3af503e1739a37d9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLALchemy(app)

from wantedtest import routes


