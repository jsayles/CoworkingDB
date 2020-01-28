from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from crdb.models import Location, Switch, VLAN, Port
from crdb.importer import Exporter

class Command(BaseCommand):
    help = "Export an Excel file"
    requires_system_checks = True

    def add_arguments(self, parser):
        parser.add_argument(
            '-f',
            action='store',
            dest='excel_file',
        )

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        try:
            exporter = Exporter(file_name=excel_file)
            print("Exporting '%s'" % exporter.file_name)
            exporter.export_data()
        except Exception as e:
            print(str(e))
            raise e
