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
