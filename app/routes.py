"""
    Defines routes
"""
from flask import render_template, session, request, url_for, redirect
#, flash, Markup
from app.server import app, cache, DEFAULT_TIMEOUT

from app.qa_bot import QaBot, NUM_QUESTIONS
from app.db import add_game

@app.route('/')
def new_game():
    session['questions'] = {}
    session['question_number'] = 1
    return render_template('new_game.html')

@app.route('/about')
@cache.cached(timeout=DEFAULT_TIMEOUT)
def about():
    return render_template('about.html')

@app.route('/question/')
def question():
    # display a question and a set of guesses
    print(session.get('questions', 'No questions'))
    bot = QaBot([])
    question_txt, options = bot.get_question()
    guesses = bot.guesses()
    return render_template(
        'question.html',
        question=question_txt,
        question_number=session.get('question_number', 1),
        options=options,
        guesses=guesses
    )

@app.route('/answer')
def answer():
    session['question_number'] = session.get('question_number', 0)+1
    # receive an answer from a user
    bot = QaBot(session['questions'])
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

    if session['question_number'] > NUM_QUESTIONS:
        return redirect(url_for('guess'))
    return redirect(url_for('question'))

@app.route('/guess')
def guess():
    bot = QaBot(session.get('questions', {}))
    guesses = bot.guesses()
    return render_template(
        'guess.html',
        guesses=guesses
    )

@app.route('/feedback/', defaults={'solution': None}, methods=['GET', 'POST'])
@app.route('/feedback/<solution>', methods=['GET', 'POST'])
def feedback(solution):
    if solution is None:
        solution = request.form.get('solution')
    if solution is not None:
        # save solution and questions to data base
        questions = session.get('questions', {})
        if questions != {}:
            print("ADD GAME ", solution, questions)
            add_game(solution, questions)
    return redirect(url_for('new_game'))
