from django.contrib import admin

from rookly.common.models import (
    Business,
    SubCategory,
    Category,
    BusinessCategory,
    BusinessService, State, City,
)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessCategory)
class BusinessCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessService)
class BusinessServiceAdmin(admin.ModelAdmin):
    pass
