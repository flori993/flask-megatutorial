from flask import Flask
from .config import Config # for uncertain reason the interpreter cannot find the file, so using a relative import
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__) # app here is the actual Flask application instance
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
login = LoginManager(app)
login.login_view = 'login' # part of feature to allow content exclusively for logged in users 

from app import routes, dbmodels
