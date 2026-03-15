from django.core.management.base import BaseCommand
from ingredients.models import UnitKind

UNIT_KINDS = [
    ("weight", "Weight"),
    ("volume", "Volume"),
    ("count", "Count"),
    ("seasoning", "Seasoning"),
    ("package", "Package"),
]


class Command(BaseCommand):
    help = "Create UnitKind instances: Weight, Volume, Count, Seasoning, "\
        "Package"

    def handle(self, *args, **options):
        created = 0
        for label, descriptive_name in UNIT_KINDS:
            obj, was_created = UnitKind.objects.get_or_create(
                label=label,
                defaults={"descriptive_name": descriptive_name})
            if was_created:
                self.stdout.write(
                    self.style.SUCCESS(f"Created UnitKind: {label}"))
                created += 1
            else:
                self.stdout.write(f"UnitKind '{label}' already exists.")
        if created == 0:
            self.stdout.write(
                self.style.WARNING("No new UnitKind instances created."))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {created} UnitKind instances."))
