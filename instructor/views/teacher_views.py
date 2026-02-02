from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from instructor.models.teacher import Teacher
from instructor.forms.teacher_forms import TeacherForm
from instructor.utils import clear_messages

@login_required
def teacher_profile_detail(request):
    

    teacher, _ = Teacher.objects.get_or_create(user=request.user)
    return render(request, "instructor/teacher/detail.html", {"teacher": teacher})


@login_required
def teacher_profile_create(request):
    if Teacher.objects.filter(user=request.user).exists():
        return redirect("instructor:teacher_detail")

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            teacher.save()
            messages.success(request, "Teacher profile created successfully.")
            return redirect("instructor:teacher_detail")
    else:
        form = TeacherForm()

    return render(request, "instructor/teacher/form.html", {"form": form})


@login_required
def teacher_profile_update(request):
    clear_messages(request)

    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("instructor:teacher_detail")
    else:
        form = TeacherForm(instance=teacher)

    return render(request, "instructor/teacher/form.html", {"form": form})


@login_required
def teacher_profile_delete(request):
    teacher = get_object_or_404(Teacher, user=request.user)

    if request.method == "POST":
        teacher.delete()
        messages.success(request, "Profile deleted successfully.")
        return redirect("instructor:dashboard")

    return render(request, "instructor/teacher/confirm_delete.html", {"teacher": teacher})
