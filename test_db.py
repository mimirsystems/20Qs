"""
Test the db and query functions
"""

from app.db import db, Entry, Question, Animal

def main():
    """ Add some things to the db """
    question1 = Question("Is this a mammal?")
    test_animal = Animal("TEST")

    entry1 = Entry(question1, "Yes", test_animal)
    entry2 = Entry(question1, "No", test_animal)
    entry3 = Entry(question1, "No", test_animal)

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
