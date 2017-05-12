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

@app.route('/new')
def new_game():
    # reset the user's game state
    return render_template('new_game.html')

@app.route('/question/')
def question():
    # display a question and a set of guesses
    question_txt = "What is your favourite colour?"
    options = [("Yes", 1), ("No", 0)]
    guesses = [("kangaroo", 0.5), ("dog", 0.9), ("rabbit", 0.1)]
    return render_template(
        'question.html',
        question=question_txt,
        options=options,
        guesses=sorted(guesses, key=lambda x: -x[1])
    )


@app.route('/set/<key>/<value>', methods=['GET'])
def set_var(key, value):
    session[key] = value
    return 'ok'

@app.route('/get/<key>', methods=['POST'])
@cache.cached(timeout=10, key_prefix='session_vars')
def get_var(key):
    return session.get(key, 'not set')
