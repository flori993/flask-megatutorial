from flask import Flask
from .config import Config # for uncertain reason the interpreter cannot find the file, so using a relative import
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os


app = Flask(__name__) # app here is the actual Flask application instance
app.config.from_object(Config)
database = SQLAlchemy(app)
migrate = Migrate(app, database)
login = LoginManager(app)
login.login_view = 'login' # part of feature to allow content exclusively for logged in users 

# Logs
if not app.debug:
    # Log errors/failures and send them by email
    if app.config['MAIL_SERVER']:
        auth = None
        if (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']):
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PASSWORD']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMIN_EMAILS'], subject='flori993.dev Failure',
            credentials=auth, secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # Log file for the application
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # RotatingFileHandler is quite nice class because it rotates the logs,
    # ensuring that the log files don't grow too large when the application runs
    # for a long time. In this case the log file size is limited to 10KB and only
    # last 10 log files are kept as backup.
    file_handler = RotatingFileHandler('logs/flori993.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s in [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Flori993 startup') # Leave a mark in logs if the server has restarted

from app import routes, dbmodels, errors
