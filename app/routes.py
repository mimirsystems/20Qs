"""
    Defines routes
"""
from server import *

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/set/')
def set_var():
    session['key'] = 'value'
    return 'ok'

@app.route('/get/')
def get_var():
    return session.get('key', 'not set')
