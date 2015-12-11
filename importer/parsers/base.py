# coding=utf-8


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
            return int(value)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def _bool(value):
        value = str(value).lower()
        if value == 'true':
            return True
        elif value == 'false':
            return False


def get_value(value, value_type, from_dict=None):
    value_method = getattr(Converter, '_%s' % value_type)
    try:
        _value = from_dict[value] if from_dict else value
        return value_method(_value)
    except KeyError:
        return None


def get_list(from_dict, fields):
    if from_dict is not None:
        _r = []
        for item in from_dict:
            result = {}
            for key in fields:
                result[key] = get_value(item.find(key).text, fields[key])
            _r.append(result)
        return _r
    return {}


class BaseParser:
    def __init__(self, data):
        self._raw = self.prepare_source(data)

    def prepare_source(self, data):
        raise NotImplemented

    def parse(self):
        return {
            'events': self.get_events(),
            'places': self.get_events(),
            'schedule': self.get_events(),
        }

    def get_events(self):
        return self._raw['events']

    def get_places(self):
        return self._raw['places']

    def get_schedule(self):
        return self._raw['schedule']
