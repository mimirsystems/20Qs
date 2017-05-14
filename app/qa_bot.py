"""
    defines a 20Qs bot
"""

class QaBot(object):
    """
        Takes a dataset and a set of answered questions
        Makes guesses about good questions to ask
        and possible solutions
    """
    def __init__(self, settings):
        self.settings = settings

    def get_question(self):
        question = 'What is your favourite colour?'
        options = ['Blue', 'Green', 'Red']

        options.append('I don\'t know')
        print('Q: {}'.format(question))
        print('A: {}'.format(options))
        return (question, options)

    def give_answer(self, question, answer):
        print('Q: {}'.format(question))
        print('A: {}'.format(answer))

    def guesses(self):
        guesses = [("kangaroo", 0.5), ("dog", 0.9), ("rabbit", 0.1)]
        guesses = [("kangaroo", 10.5), ("dog", 0.9), ("rabbit", -0.1)]
        return sorted(guesses, key=lambda x: -x[1])
