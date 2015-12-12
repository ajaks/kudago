# coding=utf-8
from datetime import datetime

from django.test import TestCase

from importer.parsers.xmlFeed import *


class GetValueTestCase(TestCase):
    def test_str(self):
        self.assertEqual('123', get_value(123, 'str'))
        self.assertEqual('1.2', get_value(1.2, 'str'))
        self.assertEqual('gv', get_value('gv', 'str'))

    def test_int(self):
        self.assertEqual(123, get_value(123, 'int'))
        self.assertEqual(None, get_value('gv', 'int'))

    def test_float(self):
        self.assertEqual(123, get_value(123, 'float'))
        self.assertEqual(1.3, get_value(1.3, 'float'))
        self.assertEqual(None, get_value('gv', 'float'))

    def test_bool(self):
        self.assertEqual(True, get_value('true', 'bool'))
        self.assertEqual(False, get_value('false', 'bool'))
        self.assertEqual(None, get_value(123, 'bool'))

    def test_date(self):
        self.assertEqual(datetime(2015, 12, 11), get_value('2015-12-11', 'date'))
        self.assertEqual(None, get_value('2015:12', 'date'))