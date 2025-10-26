from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Loads initial data only if database is empty'

    def handle(self, *args, **kwargs):
        # Check if database has any users
        if User.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    '→ Database already has data, skipping fixture load'
                )
            )
            return

        # Database is empty, load fixtures
        try:
            self.stdout.write('Loading initial data...')
            call_command('loaddata', 'fixtures/initial_data.json')
            self.stdout.write(
                self.style.SUCCESS('✓ Initial data loaded successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error loading fixtures: {e}')
            )
            # Don't raise - allow server to start even if fixture fails
            self.stdout.write(
                self.style.WARNING(
                    '→ Continuing without initial data...'
                )
            )
