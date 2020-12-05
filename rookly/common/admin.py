from django.contrib import admin

from rookly.common.models import Business, Category, BusinessCategory, BusinessService


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
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
