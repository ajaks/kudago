# coding=utf-8
from kudagoM.models import *
import logging

logger = logging.getLogger('importer')


def write_counters(title):
    def decorator(func):
        def wrapper(self):
            counters = {'r': 0, 'u': 0, 'n': 0}
            logger.info('Import %s.' % title)
            output = func(self, counters)
            logger.info(
                'Import %s. Done. Total: %s. Updated: %s. New: %s.' % (title, output['r'], output['u'], output['r'] - output['u']))

        return wrapper
    return decorator


class Mapper(object):
    def __init__(self, data):
        self.data = data

        self.import_events()
        self.import_places()
        self.import_schedule()

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

        counters['r'] = len(self.data['events'])
        return counters

    @write_counters('Places')
    def import_places(self, counters):
        counters['r'] = len(self.data['places'])
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

        counters['r'] = len(self.data['places'])
        return counters

    @write_counters('Schedule')
    def import_schedule(self, counters):
        events = Event.objects.all()
        places = Place.objects.all()

        def get_one(field, objects):
            item = [x for x in objects if x.external_id == field]
            if len(item):
                return item[0]

            return None

        for session_raw in self.data['schedule']:
            defaults = {
                key: session_raw[key]
                for key in ['date', 'time', 'time_till']
                }

            event = get_one(session_raw['event'], events)
            place = get_one(session_raw['place'], places)
            session, exist = Session.objects.get_or_create(event=event, place=place, defaults=defaults)

            if not exist:
                counters['u'] += 1
                for k, v in defaults.items():
                    setattr(session, k, v)
                session.save()

        counters['r'] = len(self.data['schedule'])
        return counters
