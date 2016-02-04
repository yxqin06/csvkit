#!/usr/bin/env python

import six

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from csvkit import convert


class TestConvert(unittest.TestCase):

    def test_valid_file(self):
        output = six.StringIO()

        with open('examples/test.xls', 'rb') as f:
            convert.convert(f, 'xls', output=output)

        with open('examples/testxls_converted.csv', 'r') as f:
            self.assertEquals(f.read(), output.getvalue())

    def test_invalid_format(self):
        with open('examples/dummy.csv', 'r') as f:
            self.assertRaises(ValueError, convert.convert, f, 'INVALID')

    def test_guess_fixed(self):
        self.assertEqual('fixed', convert.guess_format('testdata'))

    def test_guess_xls(self):
        self.assertEqual('xls', convert.guess_format('testdata.xls'))

    def test_guess_xls_uppercase(self):
        self.assertEqual('xls', convert.guess_format('testdata.XLS'))

    def test_guess_xlsx(self):
        self.assertEqual('xlsx', convert.guess_format('testdata.xlsx'))

    def test_guess_csv(self):
        self.assertEqual('csv', convert.guess_format('testdata.csv'))

    def test_guess_dbf(self):
        self.assertEqual('dbf', convert.guess_format('testdata.dbf'))

    def test_guess_json(self):
        self.assertEqual('json', convert.guess_format('testdata.json'))
