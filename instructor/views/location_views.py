from django.shortcuts import render

# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyB9rGI7puSG5CZXAaooSO9oQFBj7KWzCGI"></script>
# location google cloud API pass code AIzaSyB9rGI7puSG5CZXAaooSO9oQFBj7KWzCGI


def standard_location(request):
    return render(request, "location/standard_map.html")


def straight_route_map(request):
    return render(request,"location/straight_route_map.html")
