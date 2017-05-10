"""
Models a set of answers for many games of 20Qs
"""

class DataSet(object):
    """
        Stores all the previously recorded QA pairs

        Storing repeated answers as weights
    """

    def __init__(self):
        self.questions = {}

    def add_response(self, obj, question, answer):
        if question not in self.questions:
            self.questions[question] = {}
        if obj not in self.questions[question]:
            self.questions[question][obj] = {}

        count = self.questions[question][obj].get(answer, 0)

        self.questions[question][obj][answer] = count+1
