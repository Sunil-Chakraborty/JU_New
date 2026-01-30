from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from instructor.models import CustomUser, EmailOTP


def verify_otp(request):
    user_id = request.session.get("otp_user_id")
    purpose = request.session.get("otp_purpose")  # registration / forgot_password / first_login

    if not user_id or not purpose:
        messages.error(request, "Set your password for first-time login")
        return redirect("instructor:login")

    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == "POST":
        otp_input = request.POST.get("otp", "").strip()

        if len(otp_input) != 6 or not otp_input.isdigit():
            messages.error(request, "Enter a valid 6-digit OTP.")
            return redirect("instructor:verify_otp")

        otp_obj = EmailOTP.objects.filter(
            user=user,
            otp=otp_input,
            is_used=False
        ).order_by("-created_at").first()

        if not otp_obj:
            messages.error(request, "Invalid OTP.")
            return redirect("instructor:verify_otp")

        if otp_obj.is_expired():
            messages.error(request, "OTP expired. Please request a new one.")
            return redirect("instructor:verify_otp")

        # Mark OTP as used
        otp_obj.is_used = True
        otp_obj.save()

        # Mark email verified
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified"])

        # 🔥 IMPORTANT: persist user for password step
        request.session["set_password_user_id"] = user.id
        request.session["set_password_purpose"] = purpose
        

        return redirect("instructor:set_password")

    return render(request, "auth/verify_otp.html")
