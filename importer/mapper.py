# coding=utf-8
from kudagoM.models import *


class Mapper:
    def __init__(self, data):
        self.data = data
        self.import_events()

    def import_events(self):
        for event_raw in self.data['events']:
            defaults = {
                key: event_raw[key]
                for key in ['external_id', 'price', 'kids', 'title', 'text', 'description', 'stage_theatre', 'run_time',
                            'age_restricted']
                }

            defaults['type'], _ = EventType.objects.get_or_create(slug=event_raw['type'] or 'other')

            event, exist = Event.objects.get_or_create(external_id=event_raw['external_id'], defaults=defaults)

            if not exist:
                for k, v in defaults.items():
                    setattr(event, k, v)
                event.save()

            event.tags.clear()
            event.gallery.clear()
            event.persons.clear()

            for tag_raw in event_raw['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_raw)
                event.tags.add(tag)

            for image_raw in event_raw['gallery']:
                image, _ = Image.objects.get_or_create(url=image_raw)
                event.gallery.add(image)

            for person_raw in event_raw['persons']:
                person, _ = Person.objects.get_or_create(name=person_raw['name'])
                role, _ = Role.objects.get_or_create(name=person_raw['role'])
                event.person_set.create(person=person, role=role)

    def import_places(self):
        pass
