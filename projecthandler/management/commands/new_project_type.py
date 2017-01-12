from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create a new project type'

    def handle(self, *args, **options):

            try:
                print 'new project type'
            except Exception:
                raise CommandError('Error unable to create a new project type')

            self.stdout.write(self.style.SUCCESS('New project type successfully created'))
