from django.core.management.base import BaseCommand, CommandError
from sf_user.models import CustomSession, CustomUser


class Command(BaseCommand):
    help = 'Clean Guest Users Sessions'

    #def add_arguments(self, parser):
    #    parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        #for guest in CustomUser.objects.filter(is_guest_user="True"):
        #    self.stdout.write(self.style.SUCCESS(guest.username))
            try:
                CustomUser.objects.filter(is_guest_user="True").delete()
            except Exception:
                raise CommandError('Error unable to clean guest users sessions')

            self.stdout.write(self.style.SUCCESS('Successfully cleaned guest users sessions'))
