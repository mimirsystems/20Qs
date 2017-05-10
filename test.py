"""
    Plays a game of 20Qs and (hopefully) learns from it
"""

from DataSet import DataSet
from QaSet import QaSet

MAX_QUESTIONS = 20

YES = True
NO = False

def initialise_dataset(data):
    """
        Adds some basics to a dataSet
    """
    data.add_response("dog", "Does it have four legs?", YES)
    data.add_response("dog", "Does it mew?", NO)
    data.add_response("dog", "Does it bark?", YES)
    data.add_response("dog", "Does it have fur?", YES)

    data.add_response("cat", "Does it have four legs?", YES)
    data.add_response("cat", "Does it mew?", YES)
    data.add_response("cat", "Does it have two legs?", NO)
    data.add_response("cat", "Does it have fur?", YES)

    data.add_response("human", "Does it have fur?", NO)
    data.add_response("human", "Does it have four legs?", NO)
    data.add_response("human", "Does it have two legs?", YES)
    data.add_response("human", "Does it mew?", NO)
    data.add_response("human", "Does it bark?", NO)

def pose_question(question):
    """
        Ask the user for the answer to a question
    """
    print(question)
    answer = None
    while answer is None:
        answer = str(input()).lower()
        if answer[0] == 'y':
            answer = YES
        elif answer[0] == 'n':
            answer = NO
        else:
            answer = None
            print(question)
            print("Please answer with yes or no")
    return answer

def main():
    """
        Runs a game of 20Qs and produces a new dataset from it
    """
    data = DataSet()
    initialise_dataset(data)

    game = QaSet(data)
    while len(data.questions) < MAX_QUESTIONS:
        question = game.get_q()

        answer = pose_question(question)

        game.give_qa(question, answer)
        print(game.get_guesses())
    print("TOP GUESS: ", game.get_guesses()[0])


if __name__ == '__main__':
    main()
