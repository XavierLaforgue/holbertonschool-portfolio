from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser


admin.site.register(Profile)
