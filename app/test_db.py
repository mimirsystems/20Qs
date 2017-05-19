"""
Test the db and query functions
"""

from db import Entry, Question
from server import db

def main():
    db.create_all()

    question1 = Question("Is this a mammal?")

    entry1 = Entry(question1, "Yes")
    entry2 = Entry(question1, "No")
    entry3 = Entry(question1, "No")

    db.session.add(question1)
    db.session.add(entry1)
    db.session.add(entry2)
    db.session.add(entry3)

    db.session.commit()

    print(question1.count)
    print(question1.id)

    responses = question1.get_responses()
    print(responses)
    print(responses.all())

if __name__ == '__main__':
    main()
