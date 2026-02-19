from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile

# Register your models here.


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        # tells the form to use this model instead of django's User:
        model = CustomUser
        # lists the fields that should exist in the form class:
        fields = ("username", "email",  # because they are required
                  "first_name", "last_name")  # because it is reasonable


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # tells the form to use this model instead of django's User:
        model = CustomUser
        # lists the fields that should exist in the form class. It may not be
        # doing much, the most important was fixing the model to be CustomUser:
        fields = ("username", "email",
                  "first_name", "last_name")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # To add form fields to the admin panel including the email field which I
    # require for my project but it is not a django default user requirement.
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    # to control the add user page layout, define a fieldset that matches
    # CustomUserCreationForm (and avoid the built-in "usable_password"
    # pseudo-field from UserAdmin.add_fieldsets):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username",
                           "email",
                           "first_name",
                           "last_name",
                           "password1",
                           "password2"),
            },
        ),
    )


admin.site.register(Profile)
