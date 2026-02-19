from django.core.validators import RegexValidator


person_name_validator = RegexValidator(
    regex=r"^[A-Za-zÀ-ÖØ-öø-ÿ' -.]+$",
    message=(
        "Enter a valid name. Only letters, spaces, apostrophes, "
        "hyphens, and periods are allowed."
    ),
    code="invalid_name",
)
