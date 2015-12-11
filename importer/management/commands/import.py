# coding=utf-8
import importlib
import logging

from django.core.management import BaseCommand

from importer.mapper import Mapper


def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c


logger = logging.getLogger('importer')


class Command(BaseCommand):
    help = 'Imports into kudago models'

    def add_arguments(self, parser):
        parser.add_argument('parser', help='current parser')
        parser.add_argument('source', help='path to file')

        parser.add_argument('--events', nargs='*', help='list of events to be updated')
        parser.add_argument('--places', nargs='*', help='list of places to be updated')

    def handle(self, *args, **options):
        try:
            # TODO чота треш какой-то. Переделать бы
            _c = '%sParser' % options['parser']
            class_name = _c[0].upper() + _c[1:]

            parser_class = class_for_name('importer.parsers.%s' % options['parser'], class_name)
            logger.info('Use %s with %s' % (options['parser'], options['source']))

            logger.info('Parse data.')
            parser = parser_class(options['source'])
            logger.info('Parse data. Done.')

            data = parser.data

            if options['events']:
                events_list = map(int, options['events'])
                data['events'] = [x for x in data['events'] if x['external_id'] in events_list]
                data['schedule'] = [x for x in data['schedule'] if x['event'] in events_list]

            if options['places']:
                places_list = map(int, options['places'])
                data['places'] = [x for x in data['places'] if x['external_id'] in places_list]
                data['schedule'] = [x for x in data['schedule'] if x['place'] in places_list]

            Mapper(data)
        except (ImportError, AttributeError):
            print 'Make sure that you are using the correct parser'

        logger.info('Done.')
