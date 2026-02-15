from flask import Flask
from .config import Config # for uncertain reason the interpreter cannot find the file, so using a relative import

app = Flask(__name__) # app here is the actual Flask application instance
app.config.from_object(Config)

from app import routes

