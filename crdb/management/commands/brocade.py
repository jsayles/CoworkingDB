from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from crdb import models, brocade


class Command(BaseCommand):
    help = "Command the Brocade switch stacks"
    args = ""
    requires_system_checks = False

    def add_arguments(self, parser):
        parser.add_argument(
            '--print_stacks',
            action='store_true',
            dest='print_stacks',
            help='Show the VLAN data from all switch stacks',
        )

    def handle(self, *args, **options):
        if options['print_stacks']:
            self.print_stacks()

    def print_stacks(self):
        for s in models.SwitchStack.objects.all():
            stack = brocade.SwitchStack(s.name, s.ip_address, s.raw_username, s.raw_password, port=s.port)
            stack.print_stack()
            print()
