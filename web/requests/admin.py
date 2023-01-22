from django.contrib import admin
from .models import Request


class RequestAdmin(admin.ModelAdmin):
    list_display = (
        "id", "full_name", "get_username", 'created_at')

    search_fields = ("full_name", "get_username")
    list_filter = ("full_name",)
    ordering = ("-created_at",)


admin.site.register(Request, RequestAdmin)
