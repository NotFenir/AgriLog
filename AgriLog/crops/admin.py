from django.contrib import admin

from .models import Field, CropType, Cultivation


@admin.register(CropType)
class CropTypeAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "updated"]
    list_display_links = ["name"]
    search_fields = ["name"]


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ["name", "area_size", "owner", "created", "updated"]
    list_display_links = ["name"]
    list_filter = ["owner"]
    search_fields = ["name"]


@admin.register(Cultivation)
class CultivationAdmin(admin.ModelAdmin):
    list_display = ["field", "crop_type", "status", "year", "created", "updated"]
    list_filter = ["status", "year", "field", "crop_type"]
