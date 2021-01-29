from django.contrib import admin

from rookly.authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
