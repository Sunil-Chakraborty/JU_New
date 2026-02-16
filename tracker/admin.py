from django.contrib import admin
from .models import TrackLink, ClickLog

@admin.register(TrackLink)
class TrackLinkAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "target_url", "created_at")

@admin.register(ClickLog)
class ClickLogAdmin(admin.ModelAdmin):
    list_display = ("link", "ip_address", "device", "browser", "os", "clicked_at")
    list_filter = ("device", "browser", "os")
