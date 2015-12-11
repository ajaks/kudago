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

    def handle(self, *args, **options):
        try:
            # TODO чота треш какой-то. Переделать бы
            _c = '%sParser' % options['parser']
            class_name = _c[0].upper() + _c[1:]

            parser_class = class_for_name('importer.parsers.%s' % options['parser'], class_name)

            logger.info('Use %s with %s' % (options['parser'], options['source']))
            parser = parser_class(options['source'])

            logger.info('Mapper start')
            Mapper(parser.data)
        except (ImportError, AttributeError):
            print 'Make sure that you are using the correct parser'

        logger.info('Done')
