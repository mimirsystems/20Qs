"""
    defines a 20Qs bot
"""
from random import choice
import sqlalchemy
from app.db import Question, add_game #, Animal

NUM_QUESTIONS = 20

class QaBot(object):
    """
        Takes a dataset and a set of questions questions
        Makes guesses about good questions to ask
        and possible solutions
    """
    def __init__(self, serialized=None):
        self.questions = []
        self.guesses = None
        if serialized is not None:
            self.__dict__.update(serialized)

    def finish_game(self, solution):
        if solution is not None:
            # save solution and questions to data base
            print("ADD GAME ", solution, self.questions)
            add_game(solution, self.questions)

    def get_guesses(self):
        if self.guesses is not None:
            return self.guesses
        guesses = [("kangaroo", 0.5), ("dog", 0.9), ("rabbit", 0.1), ("octopus", 0.01)]
        self.guesses = guesses
        return sorted(guesses, key=lambda x: -x[1])

    def get_question(self):
        """ Return the next question to ask """
        if self.guesses is None:
            self.get_guesses()

        question_query = []
        try:
            new_questions = Question.query # .filter(~Question.id.in_(questions_asked))

            # filter / order and limit to get maximal split
            question_query = new_questions.all()
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        if question_query == []:
            return ("Sorry, I don't know this one", [])

        question = choice(question_query)
        options = ['Yes', 'No', 'Unsure']

        # print('Q: {}'.format(question))
        # print('A: {}'.format(options))

        q_txt = question.question
        if q_txt[-1] != '?':
            q_txt += '?'
        return (q_txt, options)

    def give_answer(self, question, answer):
        if question and answer:
            print('Q: {}'.format(question))
            print('A: {}'.format(answer))
            self.questions.append((question, answer))
            self.guesses = None # Reset
        return self.questions

    def undo(self):
        if self.questions != []:
            self.questions.pop()
            self.guesses = None

    def question_number(self):
        return len(self.questions)+1

    def game_finished(self):
        return self.question_number() > NUM_QUESTIONS

    def serialize(self):
        return self.__dict__
