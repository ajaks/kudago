# coding=utf-8
from kudagoM.models import *
import logging

logger = logging.getLogger('importer')


class Mapper(object):
    def __init__(self, data):
        self.data = data

        self.import_events()
        self.import_places()
        self.import_schedule()

    def write_counters(title):
        def decorator(func):
            def inner(self):
                counters = {'r': len(self.data[title.lower()]), 'u': 0, 'n': 0}
                logger.info('Import %s[%s]:' % (title, counters['r']))

                output = func(self, counters)
                logger.info(
                    'Import %s done. Totall: %s. Updated: %s. New: %s.' % (title, output['r'], output['u'], output['r'] - output['u']))

            return inner
        return decorator

    @write_counters('Events')
    def import_events(self, counters):
        for event_raw in self.data['events']:
            defaults = {
                key: event_raw[key]
                for key in ['external_id', 'price', 'kids', 'title', 'text', 'description', 'stage_theatre', 'run_time',
                            'age_restricted']
                }

            defaults['type'], _ = EventType.objects.get_or_create(slug=event_raw['type'] or 'other')

            event, exist = Event.objects.get_or_create(external_id=event_raw['external_id'], defaults=defaults)

            if not exist:
                counters['u'] += 1
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

        return counters

    @write_counters('Places')
    def import_places(self, counters):
        for place_raw in self.data['places']:
            defaults = {
                key: place_raw[key]
                for key in ['external_id', 'title', 'text', 'address', 'url', 'latitude', 'longitude']
                }

            defaults['type'], _ = PlaceType.objects.get_or_create(slug=place_raw['type'] or 'other')
            defaults['city'], _ = City.objects.get_or_create(name=place_raw['city'])

            place, exist = Place.objects.get_or_create(external_id=place_raw['external_id'], defaults=defaults)

            if not exist:
                counters['u'] += 1
                for k, v in defaults.items():
                    setattr(place, k, v)
                place.save()

            place.metros.clear()
            place.tags.clear()
            place.gallery.clear()
            place.phones.clear()
            place.work_times.clear()

            for metro_raw in place_raw['metros']:
                metro, _ = Subway.objects.get_or_create(name=metro_raw, defaults={'city': defaults['city']})
                place.metros.add(metro)

            for tags_raw in place_raw['tags']:
                tag, _ = Tag.objects.get_or_create(name=tags_raw)
                place.tags.add(tag)

            for gallery_raw in place_raw['gallery']:
                image, _ = Image.objects.get_or_create(url=gallery_raw)
                place.gallery.add(image)

            for phones_raw in place_raw['phones']:
                phone, _ = Phone.objects.get_or_create(phone=phones_raw['phone'])
                place.phones.add(phone)

            for work_times_raw in place_raw['work_times']:
                _type, _ = WorkTimeType.objects.get_or_create(slug=work_times_raw['type'] or 'other')
                work_time, _ = WorkTime.objects.get_or_create(time=work_times_raw['work_time'],
                                                              defaults={'type': _type})
                place.work_times.add(work_time)

        return counters

    @write_counters('Schedule')
    def import_schedule(self, counters):
        for session_raw in self.data['schedule']:
            defaults = {
                key: session_raw[key]
                for key in ['date', 'time', 'time_till']
                }

            event = Event.objects.get(external_id=session_raw['event'])
            place = Place.objects.get(external_id=session_raw['place'])
            session, exist = Session.objects.get_or_create(event=event, place=place, defaults=defaults)

            if not exist:
                counters['u'] += 1
                for k, v in defaults.items():
                    setattr(session, k, v)
                session.save()

        return counters
