from django.contrib.auth import login
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from instructor.models import CustomUser, EmailOTP
from instructor.services.email_service import send_otp_email
from django.conf import settings

from django.contrib.auth.decorators import login_required




def set_password(request):
    user_id = request.session.get("set_password_user_id")

    if not user_id:
        messages.error(request, "Session expired. Please try again.")
        return redirect("instructor:login")

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not password1 or not password2:
            messages.error(request, "Password fields cannot be empty.")
            return redirect("instructor:set_password")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("instructor:set_password")

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("instructor:set_password")

        user.set_password(password1)
        user.is_active = True
        user.save()

        # 🔥 REQUIRED because you have multiple auth backends
        login(
            request,
            user,
            backend="django.contrib.auth.backends.ModelBackend"
        )

        # cleanup
        request.session.pop("set_password_user_id", None)
        request.session.pop("set_password_purpose", None)
        request.session.pop("otp_user_id", None)
        request.session.pop("otp_purpose", None)

        return redirect("instructor:dashboard")

    return render(request, "auth/set_password.html")


@login_required
def change_password(request):
    if request.method == "POST":
        pwd1 = request.POST.get("password1")
        pwd2 = request.POST.get("password2")

        if pwd1 != pwd2:
            messages.error(request, "Passwords do not match.")
            return redirect("instructor:change_password")

        request.user.set_password(pwd1)
        request.user.save()
        login(request, request.user, backend="django.contrib.auth.backends.ModelBackend")

        messages.success(request, "Password changed successfully.")
        return redirect("instructor:dashboard")

    return render(request, "auth/change_password.html")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email", "").lower()

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "No account found with this email.")
            return redirect("instructor:forgot_password")

        # Generate OTP
        otp = EmailOTP.generate_otp()
        EmailOTP.objects.create(user=user, otp=otp)

        # Send OTP email
        send_otp_email(user.email, otp)

        # Store user id in session for next step
        request.session["otp_user_id"] = user.id
        request.session["otp_purpose"] = "forgot_password"

        messages.success(request, "OTP has been sent to your email.")
        return redirect("instructor:verify_otp")

    return render(request, "auth/forgot_password.html")


