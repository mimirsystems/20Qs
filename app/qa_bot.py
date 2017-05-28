"""
    defines a 20Qs bot
"""
from random import choice
import sqlalchemy
from .db import Question, Animal, Entry, add_game

NUM_QUESTIONS = 20
ANSWERS = ['Yes', 'No', 'Unsure']

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
            self.questions = serialized['questions']
            if 'guesses' in serialized:
                try:
                    self.guesses = []
                    for (name, _id, prob) in serialized['guesses']:
                        animal = Animal(name)
                        animal.id = _id
                        animal.prob = prob
                        self.guesses.append(animal)
                except ValueError:
                    print("CORRUPTED")

    def serialize(self):
        out = {'questions': self.questions}
        if self.guesses is not None:
            out['guesses'] = [(guess.name, guess.id, guess.prob) for guess in self.guesses]
        return out

    def get_guesses(self):
        """
        Get a weighted list of animals that 'best' fit our information
        """
        if self.guesses is not None:
            return self.guesses
        print("RECALCULATING GUESSES")
        self.guesses = []
        try:
            animals_query = Animal.query
            self.guesses = animals_query.all()
            for animal in self.guesses:
                animal.prob = 1 # animal.count
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        for question, answer in self.questions:
            self.guesses = adjust_guesses(self.guesses, question, answer)
        return self.guesses

    def get_question(self):
        """ Return the next question to ask """
        if self.guesses is None:
            self.get_guesses()

        question_query = []
        try:
            new_questions = Question.query.filter(~Question.id.in_([q[0] for q in self.questions]))

            # filter / order and limit to get maximal split
            question_query = new_questions.all()
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        if question_query == []:
            return ("Sorry, I don't know this one", [])

        question = choice(question_query)

        q_txt = question.question
        if q_txt[-1] != '?':
            q_txt += '?'
        return (q_txt, ANSWERS)

    def give_answer(self, question, answer):
        if question and answer:
            self.questions.append((question, answer))
            self.guesses = adjust_guesses(self.get_guesses(), question, answer)
        return self.questions

    def finish_game(self, solution):
        if solution is not None:
            print("ADD GAME ", solution, self.questions)
            # save solution and questions to data base
            add_game(solution, self.questions)

    def undo(self):
        if self.questions != []:
            self.questions.pop()
            self.guesses = None # will be recaluated

    def question_number(self):
        return len(self.questions)+1

    def game_finished(self):
        return self.question_number() > NUM_QUESTIONS


def adjust_guesses(animals, question, answer):
    """
    Takes a set of guesses and applies a question's answer probability distribution
    """
    try:
        for animal in animals:
            entries = Entry.query\
                    .filter(Entry.animal == animal)\
                    .filter(Entry.question.has(question=question))
            responses = [ent.answer for ent in entries.all()] + ANSWERS
            responses = {resp:responses.count(resp) for resp in responses}
            animal.prob *= responses[answer] / sum(responses.values())
    except sqlalchemy.exc.OperationalError as error:
        print("SQLALCHEMY ERROR: ", error)

    total_plays = sum([animal.prob for animal in animals])
    if total_plays != 0:
        for animal in animals:
            animal.prob /= total_plays

    animals = sorted(animals, key=lambda animal: -animal.prob)
    return animals
