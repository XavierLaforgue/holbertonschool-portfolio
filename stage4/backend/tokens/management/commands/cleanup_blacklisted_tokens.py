from django.core.management.base import BaseCommand
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken, OutstandingToken
    )
from django.utils import timezone


class Command(BaseCommand):
    help = 'Delete expired blacklisted and outstanding tokens.'

    def handle(self, *args, **options):
        now = timezone.now()
        # Delete blacklisted tokens whose outstanding token is expired
        expired_outstanding = (
                OutstandingToken.objects.filter(expires_at__lt=now)
            )
        expired_blacklisted = (
            BlacklistedToken.objects.filter(
                token__in=expired_outstanding)
        )
        count_blacklisted = expired_blacklisted.count()
        expired_blacklisted.delete()
        # Delete expired outstanding tokens
        count_outstanding = expired_outstanding.count()
        expired_outstanding.delete()
        self.stdout.write(
            f"Deleted {count_blacklisted} expired blacklisted tokens "
            f"and {count_outstanding} expired outstanding tokens."
        )
