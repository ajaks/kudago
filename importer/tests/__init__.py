# coding=utf-8
import os

from django.test import TestCase
from django.core import management

from kudagoM.models import *
class CommandTestCase(TestCase):

    def setUp(self):
        self.path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.xml')