from django.contrib import admin

from equities import models


@admin.register(models.Gap)
class GapAdmin(admin.ModelAdmin):
    date_hierarchy = "timestamp"
    list_display = [
        "symbol",
        "ascending",
        "prev_close",
        "open",
        "volume_above_average",
        "volume",
        "timestamp",
    ]
    list_filter = [
        "symbol",
        "ascending",
        "prev_close",
        "open",
        "volume_above_average",
        "volume",
        "timestamp",
    ]
    search_fields = ("symbol",)
