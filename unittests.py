"""
    Some basic unit tests
"""
import unittest
from sqlalchemy import exc

from app.db import Animal, Question, Entry, GameResult, get_all

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

if __name__ == '__main__':
    unittest.main()
