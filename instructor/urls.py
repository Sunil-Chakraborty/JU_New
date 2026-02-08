#http://127.0.0.1:8000/ → login or dashboard

#http://127.0.0.1:8000/instructor/... unchanged

# https://chatgpt.com/c/697645a5-3dd8-8320-b6f9-b606271c6b6e


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


from instructor.views import (teacher_views, student_feedback_views, 
     feedback_session_views, question_builder_views, student_preview_feedback, student_feedback_views) 

urlpatterns += [
    path("teacher/", teacher_views.teacher_profile_detail, name="teacher_detail"),
    path("teacher/create/", teacher_views.teacher_profile_create, name="teacher_create"),
    path("teacher/edit/", teacher_views.teacher_profile_update, name="teacher_edit"),
    path("teacher/delete/", teacher_views.teacher_profile_delete, name="teacher_delete"),

    path("feedback/session/create/",feedback_session_views.create_feedback_session,name="create_feedback_session"),    

    
    path("feedback/sessions/", feedback_session_views.feedback_sessions_list, name="feedback_sessions_list"),

    path(
        "feedback/<int:session_id>/question/create/",
        question_builder_views.create_question,
        name="create_question",
    ),
    
    path(
        "question/<int:question_id>/edit/",
        question_builder_views.edit_question,
        name="edit_question",
    ),
    
    path(
        "question/<int:question_id>/delete/",
        question_builder_views.delete_question,
        name="delete_question",
    ),
    
    path(
        "feedback/<int:session_id>/preview/",
        student_preview_feedback.preview_feedback,
        name="preview_feedback",
    ),

    path(
        "feedback/session/<int:session_id>/delete/",
        feedback_session_views.delete_feedback_session,
        name="delete_session",
    ),


    path(
        "feedback/session/<int:session_id>/qr/",
        feedback_session_views.generate_qr,
        name="generate_qr",
    ),

    
    path(
        "feedback/session/live-counts/",
        feedback_session_views.session_response_counts,
        name="session_live_counts",
    ),

    path("feedback/<uuid:token>/", student_feedback_views.public_feedback, name="public_feedback"),
    path("feedback/<uuid:token>/attendance/", student_feedback_views.mark_attendance, name="mark_attendance"),
    path("feedback/<uuid:token>/status/", student_feedback_views.feedback_status, name="feedback_status"),

    path(
        "feedback/live-attendance/",
        feedback_session_views.live_attendance_counts,
        name="live_attendance_counts"
    ),

    # Student QR access
    path(
        "feedback/<uuid:token>/",
        student_feedback_views.public_feedback,
        name="public_feedback"
    ),

    # Attendance click
    path(
        "feedback/<uuid:token>/attendance/",
        student_feedback_views.mark_attendance,
        name="mark_attendance"
    ),

    # Teacher permission polling
    path(
        "feedback/<uuid:token>/status/",
        student_feedback_views.feedback_status,
        name="feedback_status"
    ),
    
    # student feedback form (teacher preview / direct link)
    path(
        "feedback/<int:session_id>/",
        student_feedback_views.student_feedback,
        name="student_feedback"
    ),
    
    path("submit/<int:session_id>/", student_feedback_views.submit_feedback, name="submit_feedback"),

    path(
        "feedback/session/<int:session_id>/toggle/",
        feedback_session_views.toggle_feedback,
        name="toggle_feedback"
    ),
    
    path(
    "feedback/live-response-counts/",
    feedback_session_views.live_response_counts,
    name="live_response_counts"
),


]
