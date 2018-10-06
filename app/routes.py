"""
    Defines routes
"""
from random import shuffle
from os import urandom
from functools import wraps
from flask import render_template, session, request, url_for, redirect, flash
from flask_sqlalchemy import func, asc
from .server import app, cached, cache
from .qa_bot import QaBot, ANSWERS
from .db import add_question, add_animal, add_answer, game_stats,\
     Animal, Question, get_all, db, GameResult

def get_session_id():
    return ''.join('{:02x}'.format(x) for x in urandom(40))

def with_bot(function):
    """ Adds the bot from the session into the args """
    @wraps(function)
    def with_bot_wrapper(*args, **kwargs):
        session_id = session.get('session_id')
        if session_id is None:
            session_id = get_session_id()
            session['session_id'] = session_id
        cache_key = 'session/{}'.format(session_id)
        bot = QaBot(cache.get(cache_key))
        r_value = function(bot, *args, **kwargs)
        cache.set(cache_key, bot.serialize())
        return r_value
    return with_bot_wrapper

@app.route('/about')
@cached()
def about():
    return render_template('about.html', **game_stats())

@app.route('/')
@with_bot
def new_game(bot):
    bot.__init__() # clear the bot
    return render_template('new_game.html')

@app.route('/question/')
@with_bot
def question(bot):
    """
    Gets a set of guesses and a question from the bot
    and allows the user to answer it or go back
    """
    action = request.args.get('action')
    if action == 'back':
        bot.undo()

    question_ob, options = bot.get_question()
    return render_template(
        'question.html',
        question_number=bot.question_number(),
        question=question_ob,
        options=options,
        guesses=bot.get_guesses()
    )

@app.route('/answer')
@with_bot
def answer(bot):
    """ Take an answer from the player """
    bot.give_answer(
        request.args.get('question'),
        request.args.get('answer')
    )
    if bot.game_finished():
        return redirect(url_for('guess'))
    return redirect(url_for('question'))

@app.route('/guess')
@with_bot
def guess(bot):
    return render_template(
        'guess.html',
        guesses=bot.get_guesses()
    )

@app.route('/feedback/', defaults={'solution': None}, methods=['GET', 'POST'])
@app.route('/feedback/<solution>', methods=['GET', 'POST'])
@with_bot
def feedback(bot, solution):
    solution = request.form.get(
        'solution',
        solution
    )
    bot.finish_game(solution)
    return redirect(url_for('new_game'))

@app.route('/train/', defaults={'number': 15}, methods=['GET', 'POST'])
@app.route('/train/<int:number>', methods=['GET', 'POST'])
def train(number):
    """
    Takes suggestions for questions from the user
    """
    prefix = "animal/"
    question_txt = request.form.get('question')
    animals = [animal.name for animal in get_all(Animal)]
    shuffle(animals)
    if number != 0:
        animals = animals[:number]

    if question_txt is None:
        questions = get_all(Question)
        return render_template(
            'train.html',
            questions=questions,
            animals=animals,
            answers=ANSWERS,
            prefix=prefix
        )
    question_ob = add_question(question_txt)
    for key, answer_txt in request.form.items():
        if key[:len(prefix)] == prefix:
            animal_name = key[len(prefix):]
            animal = add_animal(animal_name)
            print(animal, "::", answer_txt)
            add_answer(question_ob, answer_txt, animal)
    flash('Thank you for the help!')
    return redirect(url_for('new_game'))

@app.route('/chart')
@cached()
def chart():
    labels = db.session.query(
        func.DATE(
            GameResult.time_created
        ).label('date')).group_by('date').order_by(asc('date')).all()
    labels = [date[0] for date in labels]
    query_wins = db.session.query(
        func.DATE(
            GameResult.time_created
        ).label('date'),
        GameResult.win,
        func.count(GameResult.win)
    ).group_by('date').group_by(GameResult.win)
    wins = query_wins.all()
    print(wins)
    wins_table = {}
    for date, win, g_count in wins:
        wins_table[date] = wins_table.get(date, {})
        wins_table[date][win] = g_count

    values = []
    for label in labels:
        if label in wins_table:
            wins = wins_table.get(label, {})
            values.append(wins.get(True, 0) / (wins.get(True, 1)+wins.get(False, 1)))
        else:
            values.append(None)
    return render_template('chart.html', values=values, labels=labels)

@app.route('/debug/animals')
def debug_animals_list():
    animals = get_all(Animal)
    return str(animals)

@app.route('/debug/questions')
def debug_questions_list():
    questions = get_all(Question)
    return str(questions)
