"""
Sets up the server core
"""
import os
from functools import wraps
from flask import Flask, request
from flask_cache import Cache
from flask_material import Material
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Base config
DEFAULT_CACHE = 60
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:////tmp/20qs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
Material(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# Database
db = SQLAlchemy(app)
db.create_all()

# Routing
NAV_ROUTES = ["new_game", "about", "suggest_a_question"]

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

# Caching any function
def cached(timeout=DEFAULT_CACHE, key='view/{path}s'):
    """ Sets up a function to have cached results """
    def decorator(func):
        """ Gets a cached value or calculates one """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            cache_key = key.format(*args, path=request.path, **kwargs)
            value = cache.get(cache_key)
            if value is not None:
                return value
            value = func(*args, **kwargs)
            cache.set(cache_key, value, timeout=timeout)
            return value
        return decorated_function
    return decorator
