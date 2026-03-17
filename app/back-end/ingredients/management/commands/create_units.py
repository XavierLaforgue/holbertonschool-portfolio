from django.core.management.base import BaseCommand
from ingredients.models import Unit, UnitKind


UNITS = {
    "weight": [
        ("milligram", "mg"),
        ("gram", "g"),
        ("kilogram", "kg"),
        ("ounce", "oz"),
        ("pound", "lb"),
    ],

    "volume": [
        ("milliliter", "ml"),
        ("centiliter", "cl"),
        ("liter", "l"),
        ("teaspoon", "tsp"),
        ("tablespoon", "tbsp"),
        ("fluid ounce", "floz"),
        ("cup", "cup"),
        ("pint", "pt"),
        ("quart", "qt"),
        ("gallon", "gal"),
    ],

    "count": [
        ("piece", "pc"),
        ("whole", "whole"),
        ("item", "item"),
        ("clove", "clove"),
        ("slice", "slice"),
        ("stick", "stick"),
        ("sprig", "sprig"),
        ("leaf", "leaf"),
        ("bunch", "bunch"),
    ],

    "seasoning": [
        ("pinch", "pinch"),
        ("dash", "dash"),
        ("drop", "drop"),
        ("sprinkle", "spr"),
        ("smidgen", "smid"),
    ],

    "package": [
        ("can", "can"),
        ("jar", "jar"),
        ("bottle", "btl"),
        ("package", "pkg"),
        ("bag", "bag"),
        ("box", "box"),
        ("block", "block"),
    ],
}


class Command(BaseCommand):
    help = "Create Unit instances grouped by UnitKind"

    def handle(self, *args, **options):
        created = 0

        for kind_label, units in UNITS.items():
            try:
                kind = UnitKind.objects.get(label=kind_label)
            except UnitKind.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(
                        f"UnitKind '{kind_label}' does not exist. "
                        "Run create_unit_kinds first."
                    )
                )
                continue

            for name, symbol in units:
                obj, was_created = Unit.objects.get_or_create(
                    name=name,
                    defaults={
                        "symbol": symbol,
                        "kind": kind,
                    }
                )

                if was_created:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Created Unit: {name} ({symbol}) [{kind_label}]"
                        )
                    )
                    created += 1
                else:
                    self.stdout.write(f"Unit '{name}' already exists.")

        if created == 0:
            self.stdout.write(
                self.style.WARNING("No new Unit instances created.")
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully created {created} Unit instances."
                )
            )
