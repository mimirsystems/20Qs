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

app.secret_key = os.environ.get('SECRET_KEY', 'wetriedIguess')
app.config['SECRET_KEY'] = app.secret_key

# Caching config
MEMCACHE_SERVERS = os.environ.get('MEMCACHEDCLOUD_SERVERS', '').split(';')
MEMCACHE_USERNAME = os.environ.get('MEMCACHEDCLOUD_USERNAME')
MEMCACHE_PASSWORD = os.environ.get('MEMCACHEDCLOUD_PASSWORD')

if MEMCACHE_SERVERS != []:
    app.config['SESSION_TYPE'] = 'memcached'
    app.config['SESSION_MEMCACHED'] = MEMCACHE_SERVERS[0]

# Base config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
                                                       'sqlite:////tmp/20qs.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Extensions
Material(app)
CACHE_CONFIG = {}
CACHE_CONFIG['CACHE_TYPE'] = 'simple'
CACHE_CONFIG['CACHE_DEFAULT_TIMEOUT'] = 1*60*60 # an hour
if MEMCACHE_USERNAME and MEMCACHE_PASSWORD and MEMCACHE_SERVERS:
    print("Connecting to Memcached")
    CACHE_CONFIG['CACHE_TYPE'] = 'app.flask_cache_backends.bmemcached'
    CACHE_CONFIG['CACHE_MEMCACHED_USERNAME'] = MEMCACHE_USERNAME
    CACHE_CONFIG['CACHE_MEMCACHED_PASSWORD'] = MEMCACHE_PASSWORD
    CACHE_CONFIG['CACHE_MEMCACHED_SERVERS'] = MEMCACHE_SERVERS
cache = Cache(app, config=CACHE_CONFIG)
app.cache = cache

# Database
db = SQLAlchemy(app)
db.create_all()

# Routing
NAV_ROUTES = ["new_game", "about", "train"]

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
def cached(key='view{path}'):
    """ Sets up a function to have cached results """
    def decorator(func):
        """ Gets a cached value or calculates one """
        @wraps(func)
        def decorated_function(*args, **kwargs):
            ckey = cache_key(key, *args, **kwargs)
            value = cache.get(ckey)
            if value is not None:
                return value
            print("DB HIT: \"{}\"".format(ckey))
            value = func(*args, **kwargs)
            cache.set(ckey, value)
            return value
        return decorated_function
    return decorator

def cache_key(key, *args, **kwargs):
    if '{path}' in key:
        kwargs['path'] = request.path
    key = key.format(*args, **kwargs)
    key = key.replace(" ", "_").replace("?", "")
    return key
