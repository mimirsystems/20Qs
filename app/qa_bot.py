"""
    defines a 20Qs bot
"""
from random import choice
import sqlalchemy
from app.db import Question, Animal, add_game

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

    def get_guesses(self):
        """
        Get a weighted list of animals that 'best' fit our information
        """
        if self.guesses is not None:
            print("CACHED GUESSES")
            return self.guesses

        self.guesses = [("kangaroo", 0.5), ("dog", 0.9), ("rabbit", 0.1), ("octopus", 0.01)]
        try:
            animals_query = Animal.query
            animals = animals_query.all()
            total_plays = sum([ani.count for ani in animals])
            self.guesses = [(ani.name, ani.count/total_plays) for ani in animals]
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        self.guesses = sorted(self.guesses, key=lambda x: -x[1])
        return self.guesses

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
            self.questions.append((question, answer))
            self.guesses = None # Reset
        return self.questions

    def finish_game(self, solution):
        if solution is not None:
            print("ADD GAME ", solution, self.questions)
            # save solution and questions to data base
            add_game(solution, self.questions)

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
