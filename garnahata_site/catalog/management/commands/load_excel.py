import os.path
import re
from django.core.management.base import BaseCommand, CommandError
from catalog.models import Address


class Command(BaseCommand):
    help = ('Loads the XLS file from editor to DB')
    args = ("<address_id> <xlsx>")

    def handle(self, *args, **options):
        try:
            address_id = int(args[0])
            address = Address.objects.get(pk=address_id)
        except (IndexError, ValueError, Address.DoesNotExist):
            raise CommandError(
                'First argument must be an integer id of the existing '
                'DB Address')

        try:
            file_path = args[1]

            if not os.path.exists(file_path):
                raise ValueError

        except (IndexError, ValueError):
            raise CommandError(
                'Second argument should a path to existing xlsx file')

        imported = address.import_owners(file_path)

        self.stdout.write("Imported records: %s" % imported)
