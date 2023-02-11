from django.contrib import admin

from .models import User


class UserConfig(admin.ModelAdmin):
    list_display = ("pk", "username", "email", "role", "confirmation_code",)
    empty_value_display = "--пусто--"


admin.site.register(User, UserConfig)
