from django.core.management.base import BaseCommand
from accounts.models import CustomUser, Profile
from accounts.serializers import (
    CustomUserHyperlinkedSerializer,
    CustomUserModelSerializer,
    ProfileHyperlinkedSerializer,
    ProfileModelSerializer,
)


class Command(BaseCommand):
    """Demonstrate how the account serializers behave.

    READ flow (serialization):   model instances -> serializer .data
    WRITE flow (deserialization): input dicts  -> serializer
        .validated_data / .errors

    This is not a test, just a quick visual aid you can run from
    the terminal to remember what each serializer does.
    """

    help = "Interactive-style dump of how account serializers serialize and "\
        "deserialize data."

    def pretty(self, label, value):
        """Small helper to print a label and a repr on its own block."""
        self.stdout.write(f"{label}:")
        self.stdout.write("    " + repr(value))
        self.stdout.write("")

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("============================"))
        self.stdout.write(self.style.NOTICE(" DEMO: CustomUser & Profile"))
        self.stdout.write(self.style.NOTICE("============================"))

        # 1) Show how demo instances are created
        self.stdout.write("")
        self.stdout.write(self.style.NOTICE(
            "[1] Creating or reusing demo instances")
        )

        user_defaults = {
            "email": "demo@example.com",
            "password": "secret",
            "first_name": "Demo",
            "last_name": "User",
        }
        self.pretty("User defaults used for get_or_create", user_defaults)

        user, user_was_created = CustomUser.objects.get_or_create(
            username="demo_user",
            defaults=user_defaults,
        )
        profile, profile_was_created = Profile.objects.\
            get_or_create(user=user)

        self.pretty("Resulting CustomUser instance", {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })
        self.pretty("Resulting Profile instance", {
            "id": profile.id,
            "user_id": profile.user_id,  # type: ignore[attr-defined]
            # TODO: implement mypy + django-stubs to have django-aware
            # type-checking
            "display_name": profile.display_name,
        })

        # 2) READ FLOW: serialization (model -> Python primitives via .data)
        self.stdout.write(self.style.NOTICE(
            "[2] SERIALIZE: model instances -> serializer.data"))

        # Hyperlinked serializers need real DRF views + URLs to resolve
        # their `url` fields. If you haven't set those up yet, this will
        # raise an ImproperlyConfigured error. We catch it so you can see
        # the difference vs ModelSerializer.
        self.stdout.write("")
        self.stdout.write(self.style.WARNING(
            "CustomUserHyperlinkedSerializer (read)"))
        try:
            user_h = CustomUserHyperlinkedSerializer(
                user,
                context={"request": None}
            )
            self.pretty("user_h.data", user_h.data)
        except Exception as exc:
            self.pretty("Skipped (no DRF routes yet)", exc)

        self.stdout.write(self.style.WARNING(
            "CustomUserModelSerializer (read)"))
        user_m = CustomUserModelSerializer(user)
        self.pretty("user_m.data", user_m.data)

        self.stdout.write(self.style.WARNING(
            "ProfileHyperlinkedSerializer (read)"))
        try:
            profile_h = ProfileHyperlinkedSerializer(
                profile, context={"request": None}
            )
            self.pretty("profile_h.data", profile_h.data)
        except Exception as exc:
            self.pretty("Skipped (no DRF routes yet)", exc)

        self.stdout.write(self.style.WARNING("ProfileModelSerializer (read)"))
        profile_m = ProfileModelSerializer(profile)
        self.pretty("profile_m.data", profile_m.data)

        # 3) WRITE FLOW: deserialization (input dict -> validated_data /
        # errors)
        self.stdout.write(self.style.NOTICE(
            "[3] DESERIALIZE: input data -> validated_data / errors"))

        # Example payloads you might POST to an API endpoint
        user_input = {
            "username": "new_demo_user",
            "email": "new_demo@example.com",
            "password": "secret",
            "first_name": "New",
            "last_name": "Demo",
        }
        profile_input = {
            "display_name": "New Demo Display",
            "bio": "Super short demo bio.",
        }

        self.pretty("CustomUserModelSerializer input payload", user_input)
        user_write = CustomUserModelSerializer(data=user_input)
        self.pretty("is_valid()", user_write.is_valid())
        self.pretty("data", user_write.data)
        if user_write.is_valid():
            self.pretty("validated_data", user_write.validated_data)
        else:
            self.pretty("errors", user_write.errors)

        # For Profile we need to pass the user relation explicitly
        profile_input_full = {**profile_input, "user": user.id}
        self.pretty("ProfileModelSerializer input payload",
                    profile_input_full)
        profile_write = ProfileModelSerializer(
            instance=profile,
            data=profile_input_full,
            partial=True
        )
        self.pretty("is_valid()", profile_write.is_valid())
        self.pretty("data", profile_write.data)
        if profile_write.is_valid():
            self.pretty("validated_data", profile_write.validated_data)
        else:
            self.pretty("errors", profile_write.errors)

        self.stdout.write(self.style.SUCCESS("Done. Scroll up to see:"))
        self.stdout.write("  - How demo instances were created")
        self.stdout.write("  - How they look when serialized (.data)")
        self.stdout.write("  - Example input payloads for deserialization")
        self.stdout.write("  - validated_data vs errors for each model")
