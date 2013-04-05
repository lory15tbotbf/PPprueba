# To change this template, choose Tools | Templates
# and open the template in the editor.

#------------------------------------------------------------------------------#
# IMPORTS
#------------------------------------------------------------------------------#
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, \
     session, flash
from werkzeug.routing import Rule
from flaskext.sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, TextAreaField, FileField, PasswordField, \
     validators

#------------------------------------------------------------------------------#
# FLASK APP
#------------------------------------------------------------------------------#
# Flask application and config
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#------------------------------------------------------------------------------#
# MIDDLEWARE (to serve static files)
#------------------------------------------------------------------------------#
# Middleware to serve the static files
from werkzeug import SharedDataMiddleware
import os
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/': os.path.join(os.path.dirname(__file__), 'templates',
        app.config['DEFAULT_TPL'])
})

#------------------------------------------------------------------------------#
# FUNCTIONS
#------------------------------------------------------------------------------#
from unicodedata import normalize

# Slug (https://gist.github.com/1428479)
def slug(text, encoding=None,
         permitted_chars='abcdefghijklmnopqrstuvwxyz0123456789-'):
    if isinstance(text, str):
        text = text.decode(encoding or 'ascii')
    clean_text = text.strip().replace(' ', '-').lower()
    while '--' in clean_text:
        clean_text = clean_text.replace('--', '-')
    ascii_text = normalize('NFKD', clean_text).encode('ascii', 'ignore')
    strict_text = map(lambda x: x if x in permitted_chars else '', ascii_text)
    return unicode(''.join(strict_text))

#------------------------------------------------------------------------------#
# MODELS
#------------------------------------------------------------------------------#
class User(db.Model):
    """User model - storing users in db"""
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    passwd = db.Column(db.String(30))

    def __init__(self, name=None, passwd=None):
        self.name = name
        self.passwd = passwd

#------------------------------------------------------------------------------#
# FORMS
#------------------------------------------------------------------------------#
# Create FormUser
class CreateFormUser(Form):
    """Form used to create a new post"""
    name = TextField('Name', [validators.required()])
    password = TextField('Password', [validators.required()])


# Login form
class LoginForm(Form):
    """Form used to login into the system"""
    username = TextField('Nick', [validators.required()])
    password = PasswordField('Password', [validators.required()])


#------------------------------------------------------------------------------#
# CONTROLLERS
#------------------------------------------------------------------------------#
# Hook before request (check user session)
@app.before_request
def check_user_status():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

# Index
@app.route('/')
def index():
        return render_template(app.config['DEFAULT_TPL']+'/index.html',
			    conf = app.config,
			    users = User.query.order_by(User.name.desc()).all(),)


# Add a new post
@app.route('/addUser', methods=['GET','POST'])
def addUser():
    if request.method == 'POST':
		user = User(name = request.form['name'], passwd = request.form['password'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('index'))
    return render_template(app.config['DEFAULT_TPL']+'/formUser.html',
			       conf = app.config,
			       form = CreateFormUser())


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is None:
        error = None
        if request.method=='POST':
            u = User.query.filter(User.name == request.form['username'], 
                                  User.passwd == request.form['password']).first()
            if u is None:
                error = 'Nick o Password incorrecto.'
            else:
                print u.id
                session['logged_in'] = True
                session['user_id'] = u.id
                session['user_name'] = u.name
                flash('Usted se ha conectado')
                return redirect(url_for('index'))
            
        return render_template(app.config['DEFAULT_TPL']+'/login.html',
                               conf = app.config,
                               form = LoginForm(request.form),
                               error = error)
    else:
        return redirect(url_for('index'))

# User Logout
@app.route('/logout')
def logout():
    if g.user is not None:
        session.pop('logged_in', None)
        session.pop('user_id', None)
        session.pop('user_name', None)
        flash('Usted se ha desconectado')
    return redirect(url_for('index'))

#------------------------------------------------------------------------------#
# MAIN
#------------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run()


