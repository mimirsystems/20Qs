"""
    Set up tables and query functions
"""
import datetime
from sqlalchemy import func, desc, asc, exc
from .server import db, cached

ANSWERS = ['Yes', 'No', 'Unsure']
NO_RESPONSE = {answer:1 for answer in ANSWERS} # laplace smoothing

class Entry(db.Model):
    """
    This class stores information of each entry in the survery form
    :field id: Primary key for an entry in the database
    :field answer: Column for answers to question in the entry
    :field question_id: Foreign key from Question class
    :field question: Defines a relationship such that details of
        entries associated with a question can be retrieved from the database
    """
    __tablename__ = 'entries'
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(30))
    time_created = db.Column(db.TIMESTAMP, server_default=db.func.now())
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    animal_id = db.Column(db.Integer, db.ForeignKey('animals.id'))

    question = db.relationship('Question', backref=db.backref('entries', lazy='dynamic'))
    animal = db.relationship('Animal', backref=db.backref('entries', lazy='dynamic'))

    def __init__(self, question, answer, animal=None):
        """
        Constructor for Entry
        :param question: An instance of class question
        :param answer: String representation of the answer provided for the question
        """
        self.question = question
        question.increment_count()
        self.answer = answer
        self.time_created = datetime.datetime.now()
        if animal != None:
            self.animal = animal
            animal.increment_count()

    def set_answer(self, animal):
        """
        This method updates the answer column for the entry
        :param animal: An instance of the class Animal
        """
        self.animal = animal
        animal.increment_count()

    def __repr__(self):
        return "Question: " + self.question.question + " Answer: " + self.answer


class Question(db.Model):
    """
    This class stores information of a question that was asked and the number of times it was asked
    :field id: Primary key for the class in the database
    :field question: String representation of the question
    :field count: Column that stores the number of times this question was asked
    """
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(200))
    count = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('question'), )


    def __init__(self, question):
        """
        Constructor
        :param question: String representation of the question asked
        """
        self.question = question
        self.count = 0

    def increment_count(self):
        """
        This method increments the count that stores the number of times the question was asked
        """
        self.count += 1

    def get_question_string(self):
        """
        This method returns the string representation of a question
        :return: String representation of the question
        """
        return self.question

    def get_responses(self):
        query = Entry.query.filter_by(question_id=self.id)
        return query

    def __repr__(self):
        return self.question + "(Asked: " + str(self.count) + " times)"


class Animal(db.Model):
    """
    This class stores information of a question that was asked and the number of times it was asked
    :field id: Primary key for the class in the database
    :field name: String representation of the animal's name
    :field count: Column that stores the number of times this animal was chosen by a user
    """
    __tablename__ = 'animals'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    count = db.Column(db.Integer)
    __table_args__ = (db.UniqueConstraint('name'), )

    def __init__(self, name):
        """
        Constructor
        :param name: String representation of the name of the animal
        """
        self.name = name
        self.count = 0

    def get_name(self):
        """
        "return: The name of the animal
        """
        return self.name

    def increment_count(self):
        """
        This method increments the count for the number of times this animal was chosen by a user
        """
        self.count += 1

    def __repr__(self):
        return "{} (x{})".format(self.name, self.count)


class GameResult(db.Model):
    """
    This class stores information of each entry in the survery form
    :field id: Primary key for a game record in the database
    :field time_created: Game finish time
    :field win: Was the game a success
    :field solution: Foreign key from Animal class
    :field guess: Top guess (ForeignKey from Animal class)
    """
    __tablename__ = 'game_results'
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.TIMESTAMP, server_default=db.func.now())
    win = db.Column(db.Boolean())
    solution = db.Column(db.String(30))
    guess = db.Column(db.String(30))

    def __init__(self, solution, guess):
        self.win = (solution == guess)
        self.solution = solution
        self.guess = guess

    def __repr__(self):
        if self.win:
            return "Game won ({})".format(self.solution)
        return "Game lost (Guessed {}, Solution {})".format(self.guess, self.solution)


def log_game(solution, guesses):
    solution = add_animal(solution).name
    guess = guesses[0].name
    log = GameResult(solution, guess)
    db.session.add(log)
    db.session.commit()

def add_game(animal_name, questions, batch=False):
    """
    Adds the data from a game to the database
    """
    if isinstance(questions, dict):
        questions = questions.items()

    animal = add_animal(animal_name, batch=batch)
    for question_txt, answer_txt in questions:
        question = add_question(question_txt, batch=batch)
        add_answer(question, answer_txt, animal, batch=batch)

def add_animal(animal_name, batch=False):
    """ Add an animal if not already found, then return it """
    animal_name = animal_name.lower().strip()
    animal = Animal.query.filter(Animal.name == animal_name).first()
    if animal is None:
        animal = Animal(animal_name)
        db.session.add(animal)
    if not batch:
        db.session.commit()
    return animal

def add_question(question_txt, batch=False):
    """ Add a question if not already found, then return it """
    question = Question.query.filter(Question.question == question_txt).first()
    if question is None:
        if question_txt == '':
            return
        if question_txt[-1] != '?':
            question_txt += '?'
        question = Question(question_txt)
        db.session.add(question)
        if not batch:
            db.session.commit()
    return question

def add_answer(question, answer_txt, animal, batch=False):
    """ Add an entry """
    if question is None or answer_txt is None or animal is None:
        return
    answer = Entry(question, answer_txt, animal)
    db.session.add(answer)
    if not batch:
        db.session.commit()
    return answer

@cached(key='all/{0.__name__}')
def get_all(class_ob):
    try:
        return set(class_ob.query.all())
    except exc.OperationalError as error:
        print("SQLALCHEMY ERROR: ", error)
    return set()

@cached(key='all_responses/{}')
def query_all_responses(question, animals=None):
    """
    Finds the counts of all responses for all animals for a particular question

    Optionally takes an animals list if only interested in a subset
    or it the list of all animals has been precomputed
    """
    try:
        if animals is None:
            animals = get_all(Animal)
        animals = {animal.id: animal for animal in animals}

        entries = db.session\
                .query(
                    Entry.animal_id,
                    Entry.answer,
                    func.count()
                ).filter(
                    Entry.question.has(question=question)
                ).group_by(Entry.animal_id, Entry.answer)

        responses = {}
        for (animal, answer, count) in entries.all():
            animal = animals.get(animal)
            if animal is not None:
                name = animal.name
                if name not in responses:
                    responses[name] = NO_RESPONSE
                responses[name][answer] += count
        return responses
    except exc.OperationalError as error:
        print("SQLALCHEMY ERROR: ", error)
    return {}

def game_stats():
    """ Get some stats about the game """
    wins = GameResult.query.filter(GameResult.win.is_(True)).count()
    losses = GameResult.query.filter(GameResult.win.is_(False)).count()
    top_solutions = db.session.query(
        func.count(GameResult.solution).label('qty'),
        GameResult.solution).group_by(GameResult.solution).order_by(desc('qty')).limit(5).all()
    bot_solutions = db.session.query(
        func.count(GameResult.solution).label('qty'),
        GameResult.solution).group_by(GameResult.solution).order_by(asc('qty')).limit(5).all()

    return wins, losses, top_solutions, bot_solutions
