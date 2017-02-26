from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Delete a project type'

    def handle(self, *args, **options):

            try:
                print 'delete project type'
            except Exception:
                raise CommandError('Error unable to delete a new project type')

            self.stdout.write(self.style.SUCCESS('Project type successfully deleted'))
