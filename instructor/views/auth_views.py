from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from instructor.models import CustomUser, EmailOTP, InstructorEmailVerification 
from instructor.services.email_service import send_otp_email

from instructor.utils import generate_otp






def login_view(request):
    email=""
    password=""
    if request.method == "POST":
        email = request.POST.get("email", "").lower().strip()
        password = request.POST.get("password", "").strip()

        try:
            user_obj = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "Account does not exist, require New Registration.")
            return redirect("instructor:login")

        # 🔐 FIRST TIME LOGIN (no password yet)
        if not user_obj.has_usable_password():
            otp = EmailOTP.generate_otp()
            EmailOTP.objects.create(user=user_obj, otp=otp)
            #send_otp_email(user_obj.email, otp)

            request.session["otp_user_id"] = user_obj.id
            request.session["otp_purpose"] = "first_login"

            messages.success(request, "Email verified successfully. Please set your password.")           
          
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


def send_otp(request, instructor):
    otp = generate_otp()

    verification, _ = InstructorEmailVerification.objects.update_or_create(
        instructor=instructor,
        defaults={"otp": otp, "is_verified": False}
    )

    # send_mail(...)  ← your existing email logic

    messages.success(request, "OTP sent to your email.")
    return redirect("verify_otp")


def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = request.POST.get("otp")

        record = InstructorEmailVerification.objects.filter(
            instructor__email=email,
            otp=otp,
            is_verified=False
        ).first()

        if record:
            record.is_verified = True
            record.save()

            messages.success(request, "Email verified successfully.")
            return redirect("login")

        messages.error(request, "Invalid OTP.")
        return redirect("verify_otp")
