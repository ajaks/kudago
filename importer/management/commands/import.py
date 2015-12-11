# coding=utf-8
import importlib
import logging

from django.core.management import BaseCommand

from importer.mapper import Mapper

logger = logging.getLogger('importer')


def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c


class Command(BaseCommand):
    help = 'Imports into kudago models'

    def add_arguments(self, parser):
        parser.add_argument('parser', help='current parser')
        parser.add_argument('source', help='path to file')

        parser.add_argument('--events', nargs='*', help='list of events to be updated')
        parser.add_argument('--places', nargs='*', help='list of places to be updated')

        parser.add_argument('-c', '--clean', action='store_true', help='Run only parser')

    def handle(self, *args, **options):
        try:
            # TODO чота треш какой-то. Переделать бы
            _c = '%sParser' % options['parser']
            class_name = _c[0].upper() + _c[1:]

            parser_class = class_for_name('importer.parsers.%s' % options['parser'], class_name)
            logger.info('Use %s with %s' % (options['parser'], options['source']))

            logger.info('Parse data.')
            parser = parser_class(options['source'])
            data = parser.data
            logger.info('Parse data. Done.')

            events_list, places_list = None, None

            if options['events']:
                events_list = map(int, options['events'])
                data['events'] = filter(lambda x: x['external_id'] in events_list, data['events'])

            if options['places']:
                places_list = map(int, options['places'])
                data['places'] = filter(lambda x: x['external_id'] in places_list, data['places'])

            if events_list or places_list:
                data['schedule'] = []
                try:
                    if len(events_list) is 1:
                        data['places'] = []
                    elif len(places_list) is 1:
                        data['events'] = []
                except TypeError:
                    pass

            if not options['clean']:
                Mapper(data)

        except (ImportError, AttributeError):
            print 'Make sure that you are using the correct parser'

        logger.info('Done.')
