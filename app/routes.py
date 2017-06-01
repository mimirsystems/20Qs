"""
    Defines routes
"""
import random
from functools import wraps
from flask import render_template, session, request, url_for, redirect
#, flash, Markup
from .server import app, cached
from .qa_bot import QaBot, ANSWERS
from .db import add_question, add_answer, game_stats, Animal, get_all

def with_bot(func):
    @wraps(func)
    def with_bot_wrapper(*args, **kwargs):
        bot = QaBot(session.get('bot'))
        r_value = func(bot, *args, **kwargs)
        session['bot'] = bot.serialize()
        return r_value
    return with_bot_wrapper

@app.route('/about')
@cached()
def about():
    wins, losses, top_solutions, bot_solutions = game_stats()
    return render_template(
        'about.html',
        wins=wins,
        losses=losses,
        top_solutions=top_solutions,
        bot_solutions=bot_solutions
    )

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

@app.route('/suggest/', defaults={'question_txt': None}, methods=['GET', 'POST'])
@app.route('/suggest/<question_txt>', methods=['GET', 'POST'])
def suggest_a_question(question_txt):
    """
    Takes suggestions for questions from the user
    """
    question_txt = request.form.get(
        'question',
        question_txt
    )
    if question_txt is None:
        return render_template(
            'suggest_question.html',
            question=question_txt
        )

    add_question(question_txt)
    animal = request.form.get('animal')
    answer_txt = request.form.get('answer')
    if animal and answer_txt:
        add_answer(question_txt, animal.name, answer_txt)

    animal = random.choice(Animal.query.all()) # Get an animal that we don't have an answer for

    return render_template(
        'suggest_question_answer.html',
        question=question_txt,
        animal=animal.name,
        options=ANSWERS
    )

@app.route('/debug/animals')
@cached()
def debug_animals_list():
    return get_all(Animal)
