"""
    Set up tables and query functions
"""
import datetime
from app.server import db

def add_game(name, questions, batch=False):
    """
    Adds the data from a game to the database
    """

    if isinstance(questions, dict):
        questions = questions.items()

    animal = Animal.query.filter(Animal.name == name).first()
    if animal is None:
        animal = Animal(name)
        db.session.add(animal)
    for question_txt, answer_txt in questions:
        question = Question.query.filter(Question.question == question_txt).first()
        if question is None:
            question = Question(question_txt)
            db.session.add(question)
        answer = Entry(question, answer_txt, animal)
        db.session.add(answer)
    if not batch:
        db.session.commit()


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
        return "{}, (was solution {} times)".format(self.name, self.count)
