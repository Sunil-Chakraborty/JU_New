from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def home(request):
    if request.user.is_authenticated:
        return redirect("instructor:dashboard")
    return redirect("instructor:login")
