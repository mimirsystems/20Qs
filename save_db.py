""" Save all the entries as aggregates """

import csv
from app.db import db, Entry
NO = 0
YES = 1
UNSURE = 2

ANSWERS = {
    'Yes': YES,
    'No': NO,
    'Unsure': UNSURE
}

def save_into_csv():
    statistics = read_into_dict()
    with open('datasets/back_up.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        writer.writerow(['Question', 'Answer', 'Animal'])

        for (question, animal) in statistics:
            stats = statistics[question, animal]
            row = [question, animal]+list(stats)
            writer.writerow(row)


def read_into_dict():
    statistics = {}
    entries = db.session.query(Entry).all()
    for entry in entries:
        stats = statistics.get((entry.question, entry.animal), [0, 0, 0])
        index = ANSWERS.get(entry.answer, UNSURE)
        stats[index] += 1
        statistics[entry.question, entry.animal] = stats

    return statistics


if __name__ == '__main__':
    save_into_csv()
