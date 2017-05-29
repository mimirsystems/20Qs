from app.db import Animal, Question
from app.db import Entry
from app.server import db
import csv

def save_to_csv():

    entries = db.session.query(Entry).all()
    
    with open('datasets/back_up.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        writer.writerow(['Question', 'Answer', 'Animal'])

        for entry in entries:

            row = [entry.question, entry.answer, entry.animal]
            writer.writerow(row)

