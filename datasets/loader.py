"""
Loads a dataset from its base file using a mapper defined for that dataset
"""

import csv

from zoo.features import FEATURES

YES_NO_MAP = {
    '0':'No',
    '1':'Yes',
    False:'No',
    True:'Yes',
}

def mapper(row):
    solution = None
    questions = {}

    for value, (question, answers) in zip(row, FEATURES):
        if answers is None:
            solution = value
        else:
            if '{}' in question: # convert a value question to a yes/no question
                for answer in answers:
                    fquestion = question.format(answer)
                    questions[fquestion] = YES_NO_MAP[value == answer]
            else: # already a yes / no question
                if value in YES_NO_MAP:
                    questions[question] = YES_NO_MAP[value]
                else:
                    raise Exception(
                        "Parse fail: Answer = {} for Question = {}".format(value, question)
                    )

    return solution, questions

def get_games_from_csv(file_name):
    """
    Takes the name of the csv file which has the zoo dataset
    and writes the samples in the format of the database
    :param file_name: Name of the file which has the zoo dataset
    """
    games = []
    with open(file_name, 'r') as csv_in_file:
        reader = csv.reader(csv_in_file)
        #Read each row from the csv and map it to a game
        games = [mapper(row) for row in reader]
    #Return the list
    return games

def add_game(solution, answers):
    """
    Takes in the solution and the dict containing all the questions
    and answers and writes them into a csv file
    :param solution: String representation of the name of the answer
    :param answer_dict: Dict with questions as keys and answers (Yes/No) as values
    """

    #with open('ZooQAs.csv', 'a') as csv_out_file:
        #writer = csv.writer(csv_out_file)

    for question, answer in answers.items():
        print("\"{}\", \"{}\", \"{}\"".format(solution, question, answer))
        #row = [question, answer_dict[question], solution]
        #writer.writerow(row)

def load_data():
    dataset = get_games_from_csv('zoo.csv')
    for game in dataset:
        add_game(*game)

if __name__ == '__main__':
    load_data()
