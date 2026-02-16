from django.urls import path
from .views import track_redirect, report

app_name = "tracker"

urlpatterns = [
    path("r/<slug:slug>/", track_redirect, name="track_redirect"),
    path("report/<slug:slug>/", report, name="report"),
]
