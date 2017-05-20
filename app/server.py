"""
Sets up the server core
"""
import os
from flask import Flask
from flask_cache import Cache
from flask_material import Material
from flask_sqlalchemy import SQLAlchemy

# Forms
# from flask_wtf import Form
# from flask_wtf.file import FileField
# from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    # BooleanField, SubmitField, IntegerField, FormField, validators
# from wtforms.validators import Required


app = Flask(__name__)

# Base config
DEFAULT_TIMEOUT = 60
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/20qs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
Material(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# Database
db = SQLAlchemy(app)
db.create_all()

# Routing
NAV_ROUTES = ["new_game", "about"]

# Colours
COLOURS = {
    'nav': 'black',
    'nav_text': 'white-text',
    'primary': 'black',
    'primary_text': 'white-text',
    'highlight': 'grey'
}

# GLOBAL DATA
@app.context_processor
def template_global_variables():
    globs = {
        'colour': COLOURS,
        'navs': NAV_ROUTES
    }
    return globs
