"""
    defines a 20Qs bot
"""
from random import choice
import sqlalchemy
from sqlalchemy.ext.serializer import loads, dumps
from .db import Question, Animal, Entry, add_game

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
            self.guesses = loads(self.guesses)

    def serialize(self):
        return {
            'questions': self.questions,
            'guesses': dumps(self.guesses)
        }

    def get_guesses(self):
        """
        Get a weighted list of animals that 'best' fit our information
        """
        if self.guesses is not None:
            print("CACHED GUESSES")
            return self.guesses
        print("RECALCULATING GUESSES")
        animals = []
        try:
            animals_query = Animal.query
            animals = animals_query.all()
            for animal in animals:
                animal.prob = animal.count

            for animal in animals:
                for question, answer in self.questions:
                    entries = Entry.query\
                            .filter(Entry.animal == animal)\
                            .filter(Entry.question.has(question=question))
                    responses = [ent.answer for ent in entries.all()] + ['Yes', 'No', 'Unsure']
                    responses = {resp:responses.count(resp) for resp in responses}
                    animal.prob *= responses[answer] / sum(responses.values())
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        total_plays = sum([animal.prob for animal in animals])
        for animal in animals:
            animal.prob /= total_plays
        self.guesses = sorted(animals, key=lambda animal: -animal.prob)
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
