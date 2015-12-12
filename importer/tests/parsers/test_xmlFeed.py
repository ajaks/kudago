# coding=utf-8
from datetime import datetime

from django.test import TestCase

from importer.parsers.xmlFeed import *


class XmlParserTestCase(TestCase):
    def setUp(self):
        self.parser = XmlFeedParser('''
        <feed>
            <events>
                <event id="1" price="false" type="other" kids="true">
                    <title><![CDATA[Boom Title]]></title>
                    <text><![CDATA[Everytext]]></text>
                    <description><![CDATA[Description]]></description>
                    <stage_theatre>StageOnTheWater</stage_theatre>
                    <runtime>120</runtime>
                    <age_restricted>19+</age_restricted>
                    <tags><tag>big</tag><tag>boom</tag></tags>
                    <persons><person><name>Bruce Wayne</name><role>batman</role></person></persons>
                    <gallery><image href="http://example.com/image.png"/></gallery>
                </event>
            </events>
            <places>
                <place id="1" type="other">
                    <title>Arkham Asylum</title>
                    <text><![CDATA[Text]]></text>
                    <address>outskirts</address>
                    <url>http://example.com/</url>
                    <coordinates latitude="32.7" longitude="45.6"/>
                    <city>Gotham</city>
                    <metros><metro>Metro</metro></metros>
                    <tags><tag>tag</tag></tags>
                    <gallery><image href="http://example.com/image.jpg"/></gallery>
                    <phones><phone type="other">797978555</phone></phones>
                    <work_times><work_time type="openhours">Always</work_time></work_times>
                </place>
            </places>
            <schedule>
                <session date="2015-12-11" event="1" place="1" time="14:00" timetill="21:30"/>
            </schedule>
        </feed>
        ''')

        self.event = {
            'external_id': 1,
            'price': False,
            'type': 'other',
            'gallery': ['http://example.com/image.png'],
            'title': 'Boom Title',
            'tags': ['big', 'boom'],
            'age_restricted': 19,
            'text': 'Everytext',
            'persons': [{'name': 'Bruce Wayne', 'role': 'batman'}],
            'run_time': 120,
            'kids': True,
            'description': 'Description',
            'stage_theatre': 'StageOnTheWater'
        }

        self.place = {
            'external_id': 1,
            'title': 'Arkham Asylum',
            'latitude': 32.7,
            'longitude': 45.6,
            'text': 'Text',
            'gallery': ['http://example.com/image.jpg'],
            'phones': [{'type': 'other', 'phone': '797978555'}],
            'metros': ['Metro'],
            'type': 'other',
            'tags': ['tag'],
            'city': 'Gotham',
            'address': 'outskirts',
            'work_times': [{'type': 'openhours', 'work_time': 'Always'}],
            'url': 'http://example.com/'
        }

        self.session = {
            'date': datetime(2015, 12, 11, 0, 0),
            'event': 1,
            'place': 1,
            'time': '14:00',
            'time_till': '21:30'
        }

    def test_parse_events(self):
        self.assertEqual([self.event], self.parser.parse_events())

    def test_parse_places(self):
        self.assertEqual([self.place], self.parser.parse_places())

    def test_parse_schedule(self):
        self.assertEqual([self.session], self.parser.parse_schedule())

    def test_parse_all(self):
        self.assertEqual(
            {
                'events': [self.event],
                'places': [self.place],
                'schedule': [self.session]
            },
            self.parser.data
        )
