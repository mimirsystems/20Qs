"""
Sets up the server core
"""
from flask import Flask
from flask_cache import Cache
from flask_material import Material

# Forms
# from flask_wtf import Form
# from flask_wtf.file import FileField
# from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    # BooleanField, SubmitField, IntegerField, FormField, validators
# from wtforms.validators import Required


app = Flask(__name__)

# Extensions
Material(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

DEFAULT_TIMEOUT = 60

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
