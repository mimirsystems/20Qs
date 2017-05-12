"""
    Defines routes
"""
from flask import render_template, session
#, flash, Markup
from server import app, cache, DEFAULT_TIMEOUT

@app.route('/')
@cache.cached(timeout=DEFAULT_TIMEOUT)
def home():
    return render_template('home.html')

@app.route('/about')
@cache.cached(timeout=DEFAULT_TIMEOUT)
def about():
    return render_template('about.html')

@app.route('/set/<key>/<value>', methods=['GET'])
def set_var(key, value):
    session[key] = value
    return 'ok'

@app.route('/get/<key>', methods=['POST'])
@cache.cached(timeout=10, key_prefix='session_vars')
def get_var(key):
    return session.get(key, 'not set')
