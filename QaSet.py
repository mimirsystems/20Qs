"""
Models a set of questions and answers
"""

from random import uniform

class QaSet(object):
    """
    Models an instance of a set of questions and answers
    """
    def __init__(self, data):
        # the data already learnt
        self.dataset = data

        # the questions and guess data currently in play
        self.questions = {}
        self.guesses = {}

    def get_q(self):
        """
        Choose a question from the dataset that hasn't been asked yet
        """
        max_utility = 0
        max_question = "ERROR, RUN OUT OF QUESTIONS"
        for question in self.dataset.questions:
            if question not in self.questions:
                # calculate the utility of this question
                utility = uniform(0, 1)
                print("\tU("+question+") = "+str(utility))
                if utility > max_utility:
                    max_utility = utility
                    max_question = question
        return max_question

    def give_qa(self, question, answer):
        print("Q:"+question)
        print("A:"+str(answer))
        self.questions[question] = answer

    def get_guesses(self):
        return self.guesses
