# coding=utf-8
import xml.etree.ElementTree as eT

from base import *


def get_attr(key, output_type, data):
    if data is not None:
        return get_value(key, output_type, data.attrib)
    return None


def get_dict(key, output_type, data, attribute=None):
    if attribute:
        return [get_attr(attribute, output_type, item) for item in data.find(key)]
    return [get_value(item.text, output_type) for item in data.find(key)]


def get_list(fields, data, attributes=None):
    if data is not None:
        _r = []
        for item in data:
            result = {}
            for key in fields:
                value = item.find(key)
                # ЧОЗАНАХУЙ ТУТ ТВОРИТСЯ?
                if value is None:
                    value = item

                result[key] = get_value(value.text, fields[key])

                if attributes is not None:
                    for attribute in attributes:
                        result[attribute] = get_attr(attribute, attributes[attribute], value)

            _r.append(result)
        return _r
    return []


class XmlFeedParser(BaseParser):
    def prepare_source(self, data):
        parser = eT.XMLParser(encoding="utf-8")
        tree = eT.parse(data, parser=parser)
        root = tree.getroot()
        return {
            'events': root[0],
            'places': root[1],
            'schedule': root[2]
        }

    def get_events(self):
        def clear_age(data):
            age = get_value('age_restricted', 'str', data)
            if age:
                return int(age.strip('+'))

            return None
        events = []
        for row in self.raw_data['events']:
            children = {child.tag: child.text for child in row}
            # logger.info(get_list({'name': 'str', 'role': 'str'}, row.find('persons')))
            event = {
                'external_id': get_value('id', 'int', row.attrib),
                'type': get_value('type', 'str', row.attrib),
                'price': get_value('price', 'bool', row.attrib),
                'kids': get_value('kids', 'bool', row.attrib),
                'title': get_value('title', 'str', children),
                'text': get_value('text', 'str', children),
                'description': get_value('description', 'str', children),
                'stage_theatre': get_value('stage_theatre', 'str', children),
                'age_restricted': clear_age(children),
                'run_time': get_value('runtime', 'int', children),
                'tags': get_dict('tags', 'str', row),
                'gallery': get_dict('gallery', 'str', row, 'href'),
                'persons': get_list({'name': 'str', 'role': 'str'}, row.find('persons')),
            }

            events.append(event)
        return events

    def get_places(self):
        places = []
        for row in self.raw_data['places']:
            children = {child.tag: child.text for child in row}
            place = {
                'external_id': get_value('id', 'int', row.attrib),
                'title': get_value('title', 'str', children),
                'text': get_value('text', 'str', children),
                'address': get_value('address', 'str', children),
                'url': get_value('url', 'str', children),
                'latitude': get_attr('latitude', 'float', row.find('coordinates')),
                'longitude': get_attr('longitude', 'float', row.find('coordinates')),
                'type': get_value('type', 'str', row.attrib),
                'city': get_value('city', 'str', children),
                'metros': get_dict('metros', 'str', row),
                'tags': get_dict('tags', 'str', row),
                'gallery': get_dict('gallery', 'str', row, 'href'),
                'phones': get_list({'phone': 'str'}, row.find('phones'), {'type': 'str'}),
                'work_times': get_list({'work_time': 'str'}, row.find('work_times'), attributes={'type': 'str'}),
            }
            places.append(place)
        return places

    def get_schedule(self):
        sessions = []
        for row in self.raw_data['schedule']:
            session = {
                'date': get_attr('date', 'date', row),
                'time': get_attr('time', 'str', row),
                'time_till': get_attr('timetill', 'str', row),
                'event': get_attr('event', 'int', row),
                'place': get_attr('place', 'int', row),
            }
            sessions.append(session)
        return sessions
