from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
import time


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = 'splite:////tmp/test.db'
db = SQLAlchemy(app)

class Entry(db.Model):
    """
    This class stores information of each entry in the survery form
    :field id: Primary key for an entry in the database
    :field answer: Column for answers to question in the entry
    :field question_id: Foreign key from Question class
    :field question: Defines a relationship such that details of entries associated with a question can be retrieved
    the database
    """
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.String(3))
    time_created = db.Column(db.TIMESTAMP, server_default=db.func.now())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', backref=db.backref('entries', lazy='dynamic'))
    
    def __init__(self, question, answer):
        """
        Constructor for Entry
        :param question: An instance of class question
        :param answer: String representation of the answer provided for the question
        """
        self.question = question
        question.incrementCount()
        self.answer = answer
        self.time_created = datetime.datetime.now()


    def __repr__(self):
        return "Question: " + self.question.question + " \nAnswer: " + self.answer

   
class Question(db.Model):
    """
    This class stores information of a question that was asked and the number of times it was asked
    :field id: Primary key for the class in the database
    :field question: String representation of the question
    :field count: Column that stores the number of times this question was asked
    """
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(100))
    count = db.Column(db.Integer, autoincrement=True)

    def __init__(self, question):
        """
        Constructor
        :param question" String representation of the question asked
        """
        self.question = question
        self.count = 0
    
    def incrementCount(self):
        """
        This method increments the count that stores the number of times the question was asked
        """
        self.count += 1

    def __repr__(self):
        return self.question + " \nAsked: " + str(self.count) + " times"

