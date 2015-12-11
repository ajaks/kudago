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


def get_value(value, value_type, data=None):
    value_method = getattr(Converter, '_%s' % value_type)
    try:
        _value = data[value] if data else value
        return value_method(_value)
    except KeyError:
        return None


def get_attr(value, value_type, data):
    if data is not None:
        return get_value(value, value_type, data.attrib)

    return None


def get_list(from_dict, fields, attributes=None):
    if from_dict is not None:
        _r = []
        for item in from_dict:
            result = {}
            for key in fields:
                value = item.find(key)

                if value is None:
                    value = item

                result[key] = get_value(value.text, fields[key])
                if attributes:
                    for attribute in attributes:
                        result[attribute] = get_attr(attribute, attributes[attribute], value)

            _r.append(result)
        return _r
    return []


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
        }

    def get_events(self):
        return self.raw_data['events']

    def get_places(self):
        return self.raw_data['places']

    def get_schedule(self):
        return self.raw_data['schedule']
