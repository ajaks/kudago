# coding=utf-8
import xml.etree.ElementTree as eT

from base import *


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
        def prepare_age_restricted(data):
            age = get_value('age_restricted', 'str', data)
            if age:
                return int(age.strip('+'))

            return None

        events = []
        for row in self.raw_data['events']:
            children = {child.tag: child.text for child in row}
            event = {
                'external_id': get_value('id', 'int', row.attrib),
                'type': get_value('type', 'str', row.attrib),
                'price': get_value('price', 'bool', row.attrib),
                'kids': get_value('kids', 'bool', row.attrib),
                'title': get_value('title', 'str', children),
                'text': get_value('text', 'str', children),
                'description': get_value('description', 'str', children),
                'stage_theatre': get_value('stage_theatre', 'str', children),
                'age_restricted': prepare_age_restricted(children),
                'run_time': get_value('runtime', 'int', children),
                'tags': [tag.text for tag in row.find('tags')],
                'gallery': [get_value('href', 'str', tag.attrib) for tag in row.find('gallery')],
                'persons': get_list(row.find('persons'), {'name': 'str', 'role': 'str'}),
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
                'metros': [tag.text for tag in row.find('metros')],
                'tags': [tag.text for tag in row.find('tags')],
                'gallery': [get_value('href', 'str', tag.attrib) for tag in row.find('gallery')],
                'phones': get_list(row.find('phones'), {'phone': 'str'}, {'type': 'str'}),
                'work_times': get_list(row.find('work_times'), {'work_time': 'str'}, {'type': 'str'}),
            }
            places.append(place)
        return places
