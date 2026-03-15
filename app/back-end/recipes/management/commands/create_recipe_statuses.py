from django.core.management.base import BaseCommand
from recipes.models import RecipeStatus

STATUSES = [
    "Draft",
    "Ready",
    "Published",
    "Saved",
]


class Command(BaseCommand):
    help = "Create RecipeStatus instances: Draft, Ready, Published, Saved"

    def handle(self, *args, **options):
        created = 0
        for value in STATUSES:
            obj, was_created = RecipeStatus.objects.get_or_create(value=value)
            if was_created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created RecipeStatus: {value}"))
                created += 1
            else:
                self.stdout.write(f"RecipeStatus '{value}' already exists.")
        if created == 0:
            self.stdout.write(self.style.WARNING(
                "No new RecipeStatus instances created."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Successfully created {created} RecipeStatus instances."))
