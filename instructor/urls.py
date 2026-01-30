#http://127.0.0.1:8000/ → login or dashboard

#http://127.0.0.1:8000/instructor/... unchanged


from django.urls import path
from instructor.views.registration_views import register
from instructor.views.auth_views import login_view, logout_view
from instructor.views.otp_views import verify_otp

from instructor.views.password_views import (
    set_password,
    forgot_password,
    change_password,
)
from instructor.views.dashboard_views import dashboard


app_name = "instructor"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    path("verify-otp/", verify_otp, name="verify_otp"),
    path("set-password/", set_password, name="set_password"),
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("change-password/", change_password, name="change_password"),
    path("dashboard/", dashboard, name="dashboard"),
    
]


from instructor.views import teacher_views

urlpatterns += [
    path("teacher/", teacher_views.teacher_profile_detail, name="teacher_detail"),
    path("teacher/create/", teacher_views.teacher_profile_create, name="teacher_create"),
    path("teacher/edit/", teacher_views.teacher_profile_update, name="teacher_edit"),
    path("teacher/delete/", teacher_views.teacher_profile_delete, name="teacher_delete"),
]


