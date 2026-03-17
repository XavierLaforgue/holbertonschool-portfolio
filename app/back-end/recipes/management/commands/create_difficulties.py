from django.core.management.base import BaseCommand
from recipes.models import Difficulty

DIFFICULTIES = [
    ("Easy", 1),
    ("Medium", 2),
    ("Hard", 3),
    ("Expert", 4),
]


class Command(BaseCommand):
    help = "Create Difficulty instances: Easy, Medium, Hard, Expert"

    def handle(self, *args, **options):
        created = 0
        for label, value in DIFFICULTIES:
            obj, was_created = Difficulty.objects.get_or_create(
                label=label, defaults={"value": value})
            if was_created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created Difficulty: {label}"))
                created += 1
            else:
                self.stdout.write(f"Difficulty '{label}' already exists.")
        if created == 0:
            self.stdout.write(self.style.WARNING(
                "No new Difficulty instances created."))
        else:
            self.stdout.write(self.style.SUCCESS(
                f"Successfully created {created} Difficulty instances."))
