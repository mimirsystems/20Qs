"""
    Defines routes
"""
from flask import render_template, session, request, url_for, redirect
#, flash, Markup
from server import app, cache, DEFAULT_TIMEOUT

from qa_bot import QaBot

@app.route('/')
@cache.cached(timeout=DEFAULT_TIMEOUT)
def new_game():
    return render_template('new_game.html')

@app.route('/about')
@cache.cached(timeout=DEFAULT_TIMEOUT)
def about():
    return render_template('about.html')

@app.route('/question')
def question():
    # display a question and a set of guesses
    print(session.get('questions', 'No questions'))
    bot = QaBot([])
    question_txt, options = bot.get_question()
    guesses = bot.guesses()
    return render_template(
        'question.html',
        question=question_txt,
        options=options,
        guesses=guesses
    )

@app.route('/answer')
def answer():
    # receive an answer from a user
    bot = QaBot([])
    question_txt = request.args.get('question')
    answer_txt = request.args.get('answer')

    if question_txt and answer_txt:
        bot.give_answer(question_txt, answer_txt)
        questions = session.get('questions')
        if not questions:
            questions = {}
        questions[question_txt] = answer_txt
        session['questions'] = questions
    else:
        print("Did not receive an answer")
    return redirect(url_for('question'))

@app.route('/set/<key>/<value>')
def set_var(key, value):
    session[key] = value
    return 'ok'

@app.route('/get/<key>')
@cache.cached(timeout=10, key_prefix='session_vars')
def get_var(key):
    return str(session.get(key, 'not set'))
