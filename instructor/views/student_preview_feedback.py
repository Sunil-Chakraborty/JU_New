from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from instructor.models.question_models import FeedbackSession


@login_required
def preview_feedback(request, session_id):
    session = get_object_or_404(FeedbackSession, id=session_id)

    # Only teacher can preview
    if session.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    questions = session.questions.prefetch_related("options")

    return render(
        request,
        "instructor/preview_feedback.html",
        {
            "session": session,
            "questions": questions,
        }
    )
