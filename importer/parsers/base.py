# coding=utf-8
from datetime import datetime

import logging
logger = logging.getLogger('importer')


class Converter:
    def __init__(self):
        pass

    @staticmethod
    def _str(value):
        return u'%s' % value

    @staticmethod
    def _int(value):
        try:
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _bool(value):
        value = str(value).lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False
        return None

    @staticmethod
    def _date(value):
        try:
            return datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return None


def get_value(value, value_type, data=None):
    value_method = getattr(Converter, '_%s' % value_type)
    try:
        _value = data[value] if data else value
        return value_method(_value)
    except KeyError:
        return None


class BaseParser:
    def __init__(self, data):
        self.raw_data = self.prepare_source(data)
        self.clear_data = None

    def prepare_source(self, data):
        raise NotImplemented

    @property
    def data(self):
        if not self.clear_data:
            self.clear_data = self.parse()
        return self.clear_data

    def parse(self):
        return {
            'events': self.get_events(),
            'places': self.get_places(),
            'schedule': self.get_schedule(),
        }

    def get_events(self):
        return self.raw_data['events']

    def get_places(self):
        return self.raw_data['places']

    def get_schedule(self):
        return self.raw_data['schedule']
