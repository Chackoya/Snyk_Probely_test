from django.contrib import admin
from snyk_app.models import Finding


# ? NOTE basic admin for Finding model => check out http://localhost:8000/admin/
# ? Requires an Admin account


@admin.register(Finding)
class FindingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "target_id",
        "definition_id",
        "method",
        "url",
        "severity",
        "state",
        "last_found",
    )
    search_fields = (
        "id",
        "target_id",
        "definition_id",
        "url",
        "path",
        "method",
        "state",
    )
    list_filter = ("severity", "state")
    ordering = ("-last_found",)
