from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from coredb.models import Location, Switch, VLAN, Port
from coredb.importer import Importer

class Command(BaseCommand):
    help = "Import an Excel file"
    args = "[excel_file]"
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str)
        parser.add_argument(
            '--delete',
            action='store_true',
            dest='delete',
            help='Delete existing data first?',
        )

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        try:
            print("Importing '%s'" % excel_file)
            importer = Importer(excel_file)
            if options['delete']:
                print("Deleting existing data...")
                importer.delete_data()
            importer.import_data()
        except Exception as e:
            print(str(e))
            # raise e
