# coding=utf-8
import os

from django.test import TestCase
from django.core.management import call_command

from kudago_app.models import *


class CommandTestCase(TestCase):
    def setUp(self):
        self.parser = 'xmlFeed'
        self.source = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.xml')

    def tearDown(self):
        Session.objects.all().delete()
        Subway.objects.all().delete()
        City.objects.all().delete()
        Tag.objects.all().delete()
        WorkTime.objects.all().delete()
        Role.objects.all().delete()
        Person.objects.all().delete()
        PlaceType.objects.all().delete()
        Place.objects.all().delete()
        Event.objects.all().delete()
        EventType.objects.all().delete()

    def test_handle(self):
        self.assertEqual(0, Event.objects.count())
        self.assertEqual(0, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

        call_command('import', self.parser, self.source, silent=True, verbosity=0)

        self.assertEqual(16, Event.objects.count())
        self.assertEqual(11, Place.objects.count())
        self.assertEqual(435, Session.objects.count())

    def test_handle_events_filter(self):
        self.assertEqual(0, Event.objects.count())
        self.assertEqual(0, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

        call_command('import', self.parser, self.source, events=[93492, 93822], silent=True, verbosity=0)

        self.assertEqual(2, Event.objects.count())
        self.assertEqual(11, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

    def test_handle_places_filter(self):
        self.assertEqual(0, Event.objects.count())
        self.assertEqual(0, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

        call_command('import', self.parser, self.source, places=[16767, 10777], silent=True, verbosity=0)

        self.assertEqual(16, Event.objects.count())
        self.assertEqual(2, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

    def test_handle_events_filter_one(self):
        self.assertEqual(0, Event.objects.count())
        self.assertEqual(0, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

        call_command('import', self.parser, self.source, events=[93822], silent=True, verbosity=0)

        self.assertEqual(1, Event.objects.count())
        self.assertEqual(0, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

    def test_handle_places_filter_one(self):
        self.assertEqual(0, Event.objects.count())
        self.assertEqual(0, Place.objects.count())
        self.assertEqual(0, Session.objects.count())

        call_command('import', self.parser, self.source, places=[16767], silent=True, verbosity=0)

        self.assertEqual(16, Event.objects.count())
        self.assertEqual(1, Place.objects.count())
        self.assertEqual(0, Session.objects.count())