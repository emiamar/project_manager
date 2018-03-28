from django.core.management.base import BaseCommand

from ticket import ticket_importer

class Command(BaseCommand):
    help = 'Reports jobcards created on a perticular day'



    def handle(self, *args, **options):
        result = ticket_importer.ticket_importer()
        # if result:
        self.stdout.write(
            'Successfully imported tickets')