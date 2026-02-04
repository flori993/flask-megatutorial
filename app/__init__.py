from flask import Flask

app = Flask(__name__) # app here is the actual Flask application instance

from app import routes

