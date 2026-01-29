from instructor.forms.registration import RegistrationForm
from instructor.models import EmailOTP, CustomUser
from instructor.services.email_service import send_otp_email
from django.shortcuts import render, redirect

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_unusable_password()
            user.is_active = True
            user.save()

            otp = EmailOTP.generate_otp()
            EmailOTP.objects.create(user=user, otp=otp)

            send_otp_email(user.email, otp)

            request.session["otp_user_id"] = user.id
            return redirect("instructor:verify_otp")

    else:
        form = RegistrationForm()

    return render(request, "auth/register.html", {"form": form})
