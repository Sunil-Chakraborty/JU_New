from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    CustomUser,
    Instructor,
    Teacher,
    Department,    
    FeedbackSession,
)



@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    model = CustomUser

    list_display = (
        "email",
        "user_type",
        "is_email_verified",
        "is_active",
        "is_staff",
    )

    list_filter = (
        "user_type",
        "is_email_verified",
        "is_active",
        "is_staff",
    )

    ordering = ("email",)

    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("User Info", {"fields": ("user_type",)}),
        ("Status", {"fields": ("is_email_verified", "is_active", "is_staff")}),
        ("Permissions", {"fields": ("groups", "user_permissions")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "user_type", "password1", "password2"),
        }),
    )


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("user", "department", "created_at")
    search_fields = ("user__username",)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "designation")
    search_fields = ("user__username",)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "faculty", "program", "prog_cd")
    search_fields = ("name", "faculty")



@admin.register(FeedbackSession)
class FeedbackSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "instructor", "session_id", "created_at")
