from django.core.management.base import BaseCommand, CommandError
from sf_user.models import CustomSession


class Command(BaseCommand):
    help = 'Clean Users Sessions'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
            try:
                CustomSession.objects.all().delete()
            except Exception:
                raise CommandError('Error unable to clean users sessions')

            self.stdout.write(self.style.SUCCESS('Successfully cleaned users sessions'))