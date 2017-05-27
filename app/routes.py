"""
    Defines routes
"""
from flask import render_template, session, request, url_for, redirect
#, flash, Markup
from app.server import app, cache, DEFAULT_TIMEOUT
from app.qa_bot import QaBot

def with_bot(func):
    name = func.__name__
    def with_bot_wrapper(*args, **kwargs):
        bot = QaBot(session.get('bot'))
        r_value = func(bot, *args, **kwargs)
        session['bot'] = bot.serialize()
        return r_value
    with_bot_wrapper.__name__ = name
    return with_bot_wrapper

@app.route('/about')
@cache.cached(timeout=DEFAULT_TIMEOUT)
def about():
    return render_template('about.html')

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

    question_txt, options = bot.get_question()
    return render_template(
        'question.html',
        question_number=bot.question_number(),
        question=question_txt,
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
