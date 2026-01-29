from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from instructor.models import CustomUser, EmailOTP
from instructor.services.email_service import send_otp_email


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").lower().strip()
        password = request.POST.get("password", "").strip()

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Account does not exist.")
            return redirect("instructor:login")

        # 🔐 FIRST TIME LOGIN (no password yet)
        if not user_obj.has_usable_password():
            otp = EmailOTP.generate_otp()
            EmailOTP.objects.create(user=user_obj, otp=otp)
            send_otp_email(user_obj.email, otp)

            request.session["otp_user_id"] = user_obj.id
            request.session["otp_purpose"] = "first_login"

            messages.success(request, "OTP sent to your email.")
            return redirect("instructor:verify_otp")

        # 🔑 NORMAL LOGIN
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("instructor:dashboard")

        if user is not None:
            login(request, user)
            return redirect("instructor:dashboard")

        # ❌ WRONG PASSWORD
        messages.error(request, "Invalid email or password.")
        return redirect("instructor:login")

    return render(request, "auth/login.html")

def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("instructor:login")
