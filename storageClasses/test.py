from Entry import Entry
from Entry import Question
from Entry import db

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
