"""
    Defines routes and starts server
"""

from flask import Flask, render_template

DEBUG = True
APP = Flask(__name__)
GAME_SESSIONS = {}
LAST_GAME = 0

@APP.route('/')
def home():
    return render_template('home.html')

@APP.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    APP.run(debug=DEBUG)
