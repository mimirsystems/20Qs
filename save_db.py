""" Save all the entries as aggregates """

import csv
from app.db import Entry

<<<<<<< HEAD:saveDB.py
def save_into_csv():

    statistics = read_into_dict()

=======
def save_to_csv():
    entries = Entry.query.all()
>>>>>>> 77a7f7cfeb121c6e74fc137b1a0442994261f296:save_db.py
    with open('datasets/back_up.csv', 'w') as csv_out_file:
        writer = csv.writer(csv_out_file)
        writer.writerow(['Question', 'Answer', 'Animal'])
        
        for (question, animal) in statistics:
            li = statistics[question, animal]
            row = [question, animal]
            for entry in li:
                row.append(entry)

<<<<<<< HEAD:saveDB.py
            writer.writerow(row)


def read_into_dict():

    statistics = {}
    entries = db.session.query(Entry).all()
    
    for entry in entries:
        
        if (entry.question, entry.animal) in statistics:
            li = statistics[entry.question, entry.animal]
            index = get_value(entry.answer)
            li[index] += 1
            statistics[entry.question, entry.animal] = li
        else:
            li = [0,0,0]
            index = get_value(entry.answer)
            li[index] += 1
            statistics[entry.question, entry.animal] = li

    return statistics
                

def get_value(answer):
    NO = 0
    YES = 1
    UNSURE = 2
    if answer == 'Yes':
        return YES
    elif answer == 'NO':
        return NO
    else:
        return UNSURE

save_into_csv()
=======
        for entry in entries:
            row = [entry.question, entry.answer, entry.animal]
            writer.writerow(row)
>>>>>>> 77a7f7cfeb121c6e74fc137b1a0442994261f296:save_db.py
