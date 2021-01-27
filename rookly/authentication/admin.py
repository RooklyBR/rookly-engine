from django.contrib import admin

from rookly.authentication.models import User, State, City


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass
