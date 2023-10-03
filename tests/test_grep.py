import re
import unittest

from csvkit.exceptions import ColumnIdentifierError
from csvkit.grep import FilteringCSVReader


class TestGrep(unittest.TestCase):

    def setUp(self):
        self.tab1 = [
            ['id', 'name', 'i_work_here'],
            ['1', 'Chicago Reader', 'first'],
            ['2', 'Chicago Sun-Times', 'only'],
            ['3', 'Chicago Tribune', 'only'],
            ['1', 'Chicago Reader', 'second']]

        self.tab2 = [
            ['id', 'age', 'i_work_here'],
            ['1', 'first', '0'],
            ['4', 'only', '0'],
            ['1', 'second', '0'],
            ['2', 'only', '0', '0']]  # Note extra value in this column

    def test_pattern(self):
        fcr = FilteringCSVReader(iter(self.tab1), patterns=['1'])
        self.assertEqual(self.tab1[0], next(fcr))
        self.assertEqual(self.tab1[1], next(fcr))
        self.assertEqual(self.tab1[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_no_header(self):
        fcr = FilteringCSVReader(iter(self.tab1), patterns={2: 'only'}, header=False)
        self.assertEqual(self.tab1[2], next(fcr))
        self.assertEqual(self.tab1[3], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_regex(self):
        pattern = re.compile(".*(Reader|Tribune).*")
        fcr = FilteringCSVReader(iter(self.tab1), patterns={1: pattern})

        self.assertEqual(self.tab1[0], next(fcr))
        self.assertEqual(self.tab1[1], next(fcr))
        self.assertEqual(self.tab1[3], next(fcr))
        self.assertEqual(self.tab1[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_inverse(self):
        fcr = FilteringCSVReader(iter(self.tab2), patterns=['1'], inverse=True)
        self.assertEqual(self.tab2[0], next(fcr))
        self.assertEqual(self.tab2[2], next(fcr))
        self.assertEqual(self.tab2[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_column_names_in_patterns(self):
        fcr = FilteringCSVReader(iter(self.tab2), patterns={'age': 'only'})
        self.assertEqual(self.tab2[0], next(fcr))
        self.assertEqual(self.tab2[2], next(fcr))
        self.assertEqual(self.tab2[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_mixed_indices_and_column_names_in_patterns(self):
        fcr = FilteringCSVReader(iter(self.tab2), patterns={'age': 'only', 0: '2'})
        self.assertEqual(self.tab2[0], next(fcr))
        self.assertEqual(self.tab2[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_duplicate_column_ids_in_patterns(self):
        try:
            FilteringCSVReader(iter(self.tab2), patterns={'age': 'only', 1: 'second'})
            self.fail("Should be an exception.")
        except ColumnIdentifierError:
            pass

    def test_index_out_of_range(self):
        fcr = FilteringCSVReader(iter(self.tab2), patterns={3: '0'})
        self.assertEqual(self.tab2[0], next(fcr))
        self.assertEqual(self.tab2[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_any_match(self):
        fcr = FilteringCSVReader(iter(self.tab2), patterns={'age': 'only', 0: '2'}, any_match=True)
        self.assertEqual(self.tab2[0], next(fcr))
        self.assertEqual(self.tab2[2], next(fcr))
        self.assertEqual(self.tab2[4], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_any_match_and_inverse(self):
        fcr = FilteringCSVReader(iter(self.tab2), patterns={'age': 'only', 0: '2'}, any_match=True, inverse=True)
        self.assertEqual(self.tab2[0], next(fcr))
        self.assertEqual(self.tab2[1], next(fcr))
        self.assertEqual(self.tab2[3], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass

    def test_multiline(self):
        table = [
            ['a', 'b'],
            ['1', 'foo\nbar'],
        ]
        fcr = FilteringCSVReader(iter(table), patterns={'b': re.compile('bar')})
        self.assertEqual(table[0], next(fcr))
        self.assertEqual(table[1], next(fcr))
        try:
            next(fcr)
            self.fail("Should be no more rows left.")
        except StopIteration:
            pass
