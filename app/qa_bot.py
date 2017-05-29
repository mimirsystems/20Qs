"""
    defines a 20Qs bot
"""
from math import log2
import sqlalchemy
from .db import Question, Animal, Entry, add_game, log_game

NUM_QUESTIONS = 20
ANSWERS = ['Yes', 'No', 'Unsure']
SOLUTIONS_TO_CONSIDER = 15

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
            self.guesses = Animal.query.all()
            for animal in self.guesses:
                animal.prob = 1.0/len(self.guesses) # animal.count
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        for question, answer in self.questions:
            self.guesses = adjust_guesses(self.guesses, question, answer)
        return self.guesses

    def get_question(self):
        """ Return the next question to ask """
        best_q = {}
        try:
            new_qs = Question.query
            if self.questions != []:
                new_qs = new_qs.filter(
                    ~Question.question.in_(
                        [q[0] for q in self.questions]))
            # filter / order and limit to get maximal split
            questions = new_qs.all()
            animals = self.get_guesses()[:SOLUTIONS_TO_CONSIDER]
            for question in questions:
                split = get_entropy(question, animals)
                print("Q: {}, Entropy: {:.2f}".format(question, split))
                if split > best_q.get('split', 0): # maximize entropy
                    best_q['split'] = split
                    best_q['question'] = question
        except sqlalchemy.exc.OperationalError as error:
            print("SQLALCHEMY ERROR: ", error)

        if 'question' not in best_q:
            return ("Sorry, I don't know this one", [])

        return (best_q['question'].question, ANSWERS)

    def give_answer(self, question, answer):
        if question and answer:
            self.questions.append((question, answer))
            self.guesses = adjust_guesses(self.get_guesses(), question, answer)
        return self.questions

    def finish_game(self, solution):
        if solution is not None:
            # save solution and questions to data base
            add_game(solution, self.questions)
            #log the outcome
            log_game(solution, self.guesses)

    def undo(self):
        if self.questions != []:
            question, answer = self.questions[-1]
            self.guesses = adjust_guesses(self.guesses, question, answer, weighting=-1)
            self.questions.pop()

    def question_number(self):
        return len(self.questions)+1

    def game_finished(self):
        return self.question_number() > NUM_QUESTIONS


def get_entropy(question, animals):
    """ Finds the entropy of the answers of a question for a set of animals """
    response_set = {answer:0.000001 for answer in ANSWERS}

    for animal in animals:
        responses = query_responses(animal.name, question.question)
        responses = sorted(responses.items(), key=lambda resp: -resp[1])
        (first, _) = responses[0]
        (last, _) = responses[0]
        response_set[first] += animal.prob
        response_set[last] += (1-animal.prob)

    total = sum(response_set.values())
    probs = [count/total for count in response_set.values()]

    entropy = sum([-(p)*log2(p) for p in probs])
    return entropy


def adjust_guesses(animals, question, answer, weighting=1):
    """
    Takes a set of guesses and applies a question's answer probability distribution
    """
    try:
        for animal in animals:
            responses = query_responses(animal.name, question)
            animal.prob *= pow(responses[answer] / sum(responses.values()), weighting)
    except sqlalchemy.exc.OperationalError as error:
        print("SQLALCHEMY ERROR: ", error)

    total_plays = sum([animal.prob for animal in animals])
    if total_plays != 0:
        for animal in animals:
            animal.prob /= total_plays

    animals = sorted(animals, key=lambda animal: -animal.prob)
    return animals

def query_responses(animal, question):
    entries = Entry.query\
            .filter(Entry.animal.has(name=animal))\
            .filter(Entry.question.has(question=question))
    responses = [ent.answer for ent in entries.all()] + ANSWERS
    responses = {resp:responses.count(resp) for resp in responses}
    return responses
