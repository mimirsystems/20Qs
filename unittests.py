"""
    Some basic unit tests
"""
import unittest
from flask_sqlalchemy.SQLAlchemy import exc

from app.db import Animal, Question, Entry, GameResult, get_all, merge_animal, add_animal

TABLES = [Animal, Question, Entry, GameResult]

class TestDBs(unittest.TestCase):
    """
    Tests that the tables exist in the db
    and can be queried without crashing
    """

    def test_tables_exist(self):
        for table in TABLES:
            query = None
            try:
                query = table.query.count()
            except exc.OperationalError as error:
                print(error)
            self.assertNotEqual(query, None, 'table \'{}\' does not exist'.format(table.__name__))
        self.assertNotEqual(len(TABLES), 0, 'had no tables')

    def test_get_all(self):
        for table in TABLES:
            query_db = table.query.all()
            query_all = get_all(table)
            self.assertEqual(
                len(query_db),
                len(query_all),
                'get_all length differed to query.all() for table \'{}\''\
                .format(table.__name__)
            )
            for q_db, q_a in zip(query_db, query_all):
                self.assertEqual(
                    q_db,
                    q_a,
                    'get_all differed to query.all() for table \'{}\''\
                    .format(table.__name__)
                )

    def test_merge_move_animals(self):
        """ Check that moving via merging works properly """
        entries = sorted([(e.id, e.answer) for e in Entry.query.all()])
        weird_unique_name = '1234567890'

        weird_animal = add_animal(weird_unique_name)
        slowworm = add_animal('slowworm')

        merge_animal(slowworm, weird_unique_name, do_merge=True)
        self.assertEqual(
            Entry.query.filter(Entry.animal == slowworm).all(),
            [],
            "Merge source should not exist"
        )
        slowworm = add_animal('slowworm')
        merge_animal(weird_unique_name, slowworm, do_merge=True)
        new_entries = sorted([(e.id, e.answer) for e in Entry.query.all()])
        self.assertEqual(
            new_entries,
            entries,
            "Merge a->b, b->a should result in nop (animal id may change)"
        )
        self.assertEqual(
            Entry.query.filter(Entry.animal == weird_animal).all(),
            [],
            "Merge source should not exist"
        )

    def test_merge_two_animals(self):
        """ Check that merging two animals works properly """
        pass


if __name__ == '__main__':
    unittest.main()
