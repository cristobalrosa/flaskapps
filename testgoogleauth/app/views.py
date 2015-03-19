from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, google, login_manager
from models import User


@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@login_required
def index():
    return render_template('index.html', name=g.user.nickname)

@app.route('/login')
def login():
    print "Login"
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    print "Logout"
    session.pop('google_token', None)
    logout_user()
    return render_template('logout.html')


@login_manager.user_loader
def load_user(userid):
    user = User.query.filter_by(id=str(userid)).first()
    return user

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    authorized_users = ["email1@gmail.com", "email2@gmail.com"]
    if resp is None:
        return render_template("403.html")
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    if me.data['email'] in authorized_users:
        user = User.query.filter_by(id=str(me.data['id'])).first()
        if user:
            user.nickname = me.data['name']
        else:
            user_id = str(me.data['id'])
            user_name = str(me.data['name'])
            user_email = str(me.data['email'])
            user = User(id=user_id, nickname=user_name, email=user_email)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template("403.html")

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(401)
def page_unauthorized(e):
    return render_template('401.html'), 401
