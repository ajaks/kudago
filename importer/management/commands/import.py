# coding=utf-8
import importlib

from django.core.management import BaseCommand

from importer.mapper import Mapper


def class_for_name(module_name, class_name):
    m = importlib.import_module(module_name)
    c = getattr(m, class_name)
    return c


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
            print 'Use %s:' % class_name

            parser_class = class_for_name('importer.parsers.%s' % options['parser'], class_name)

            print '\t - parse source %s' % options['source']
            parser = parser_class(options['source'])

            print '\t - import data'
            Mapper(parser.data)
        except (ImportError, AttributeError):
            print 'Make sure that you are using the correct parser'

        print 'done'
