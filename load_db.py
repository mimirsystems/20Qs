"""
Load the db with a dataset (or multiple)
"""

from app.db import Animal, Question, add_game
from app.server import db

from datasets.loader import get_games_from_csv
from datasets.zoo.features import FEATURES

def main():
    games = get_games_from_csv('datasets/zoo/zoo.csv', FEATURES)

    for game in games:
        add_game(*game, batch=True)
    db.session.commit()

    print("Check that something went in!")
    print(Animal.query.all())
    print(Question.query.all())

if __name__ == '__main__':
    db.create_all()
    main()

