import os

class Config(object):
    # os.urandom(24).encode('hex')
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    # Go to https://console.developers.google.com/project?authuser=0 (Google Developer Console)
    # New Project
    # Go to the project-> API&auth -> credentials -> Create Client new ID-> Web Application
    GOOGLE_LOGIN_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    GOOGLE_LOGIN_CLIENT_SECRET = "xxxxxxxxxx"
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    WTF_CSRF_ENABLED = True
