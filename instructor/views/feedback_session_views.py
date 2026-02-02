from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from instructor.models.question_models import FeedbackSession

def create_feedback_session(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            FeedbackSession.objects.create(
                teacher=request.user,
                title=title
            )
            return redirect("instructor:dashboard")

    return render(request, "instructor/create_session.html")


def feedback_sessions_list(request):
    sessions = FeedbackSession.objects.filter(teacher=request.user)
    return render(request, "instructor/session_list.html", {"sessions": sessions})


@login_required
def delete_feedback_session(request, session_id):
    session = get_object_or_404(
        FeedbackSession,
        id=session_id,
        teacher=request.user   # IMPORTANT
    )

    if session.questions.exists():
        return HttpResponseForbidden(
            "Cannot delete session with questions"
        )

    session.delete()
    return redirect("instructor:feedback_sessions_list")
