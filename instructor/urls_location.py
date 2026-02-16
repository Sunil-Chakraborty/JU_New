from django.urls import path
from .views.location_views import straight_route_map

urlpatterns = [
    path("route/", straight_route_map, name="straight_route_map"),
]
