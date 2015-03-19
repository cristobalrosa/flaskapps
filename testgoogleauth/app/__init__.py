from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy

import logging
import logging.handlers
from flask.ext.login import LoginManager
from flask_oauthlib.client import OAuth


LOG_FILENAME = '/tmp/app.log'
API_LOGGER = logging.getLogger('test-logger')
LOG_HANDLER = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000, backupCount=1)

app = Flask(__name__)
app.config.from_object('app.config.Config')
app.logger.addHandler(LOG_HANDLER)
app.logger.setLevel(logging.INFO)
login_manager = LoginManager()
login_manager.init_app(app)
bootstrap = Bootstrap(app)
oauth = OAuth(app)
google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_LOGIN_CLIENT_ID'),
    consumer_secret=app.config.get('GOOGLE_LOGIN_CLIENT_SECRET'),
    request_token_params={
        'scope': 'https://www.googleapis.com/auth/userinfo.email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

db = SQLAlchemy(app)


@app.before_first_request
def before_first_request():
    try:
        db.create_all()
    except Exception, e:
        app.logger.error(str(e))

import views
import models