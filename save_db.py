""" Save all the entries as aggregates """

import csv
from app.db import Entry

def save_to_csv():
    entries = Entry.query.all()
    with open('datasets/back_up.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        writer.writerow(['Question', 'Answer', 'Animal'])

        for entry in entries:
            row = [entry.question, entry.answer, entry.animal]
            writer.writerow(row)
