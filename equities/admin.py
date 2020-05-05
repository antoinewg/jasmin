import csv

from django.contrib import admin
from django.http import HttpResponse

from equities import models


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


@admin.register(models.Gap)
class GapAdmin(admin.ModelAdmin, ExportCsvMixin):
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
    actions = ["export_as_csv"]
