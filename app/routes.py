"""
    Defines routes and starts server
"""
from flask import Flask, render_template
from flask import session
from flask_material import Material
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

from os import path, walk



app = Flask(__name__)
Material(app)

# Config
app.config['SECRET_KEY'] = 'loljk'
app.config['RECAPTCHA_PUBLIC_KEY'] = 'TEST'

GAME_SESSIONS = {}
LAST_GAME = 0

NAV_ROUTES = ["home", "about"] #, "new"]

# GLOBAL DATA
@app.context_processor
def template_global_variables():
    return dict(navs=NAV_ROUTES)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/set/')
def set():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def get():
    return session.get('key', 'not set')


if __name__ == '__main__':
    WATCH = ['templates', 'static']
    for extra_dir in list(WATCH):
        for dirname, _, files in walk(extra_dir):
            WATCH += [path.join(dirname, file) for file in files]
    app.run(host='0.0.0.0', port=8000, extra_files=WATCH, debug=True)
