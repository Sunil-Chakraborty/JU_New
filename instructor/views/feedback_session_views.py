from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from instructor.models.question_models import FeedbackSession, Question, Option
from instructor.forms import FeedbackSessionForm   # 👈 CLEAN IMPORT
from django.http import JsonResponse
from django.db.models import Count

import uuid
import qrcode
import base64
from io import BytesIO

from django.utils import timezone
from django.urls import reverse

from instructor.models.question_models import FeedbackSession



@login_required
def generate_qr(request, session_id):
    session = get_object_or_404(
        FeedbackSession,
        id=session_id,
        teacher=request.user
    )

    # Late activation: generate only once
    if not session.public_token:
        session.public_token = uuid.uuid4()
        session.qr_activated_at = timezone.now()
        session.save()

    public_url = request.build_absolute_uri(
        reverse("instructor:public_feedback", args=[session.public_token])
    )

    # Generate QR
    qr = qrcode.make(public_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(
        request,
        "instructor/feedback/qr_display.html",
        {
            "session": session,
            "public_url": public_url,
            "qr_base64": qr_base64,
        }
    )
    


@login_required
def create_feedback_session(request):
    if request.method == "POST":
        form = FeedbackSessionForm(request.POST, teacher=request.user)

        if form.is_valid():
            # 1. Create new session
            session = form.save(commit=False)
            session.teacher = request.user
            session.save()

            # 2. Copy questions + options
            copy_from = form.cleaned_data.get("copy_from")

            if copy_from:
                for q in copy_from.questions.all():
                    new_q = Question.objects.create(
                        session=session,
                        text=q.text,
                        q_type=q.q_type,
                    )

                    # 🔴 THIS BLOCK WAS NOT EXECUTING BEFORE
                    for opt in q.options.all():
                        Option.objects.create(
                            question=new_q,
                            text=opt.text
                        )

            return redirect("instructor:feedback_sessions_list")
    else:
        form = FeedbackSessionForm(teacher=request.user)

    return render(
        request,
        "instructor/create_session.html",
        {"form": form}
    )

    

def feedback_sessions_list(request):
    sessions = (
        FeedbackSession.objects
        .filter(teacher=request.user)
        .annotate(response_count=Count('responses'))  # <-- MAGIC LINE
        .order_by('-created_at')
    )
    
    # Equivalent SQL statement
    #    SELECT session.*, COUNT(feedbackresponse.id) AS response_count
    #    FROM feedbacksession
    #    LEFT JOIN feedbackresponse
    #    ON feedbacksession.id = feedbackresponse.session_id
    #    GROUP BY feedbacksession.id


    return render(request, "instructor/session_list.html", {
        "sessions": sessions
    })


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


def session_response_counts(request):
    sessions = (
        FeedbackSession.objects
        .annotate(response_count=Count("responses"))
        .values("id", "response_count")
    )

    data = {str(s["id"]): s["response_count"] for s in sessions}

    return JsonResponse(data)


def live_attendance_counts(request):
    sessions = (
        FeedbackSession.objects
        .filter(teacher=request.user, is_active=True)
        .annotate(present_count=Count("attendances"))
        .values("id", "present_count", "feedback_open")
    )

    data = {
        str(s["id"]): {
            "present": s["present_count"],
            "open": s["feedback_open"]
        }
        for s in sessions
    }

    return JsonResponse(data)


@login_required
def toggle_feedback(request, session_id):
    session = get_object_or_404(
        FeedbackSession,
        id=session_id,
        teacher=request.user
    )

    session.feedback_open = not session.feedback_open
    session.save()

    return redirect("instructor:feedback_sessions_list")    
    
    
from django.http import JsonResponse
from instructor.models.question_models import FeedbackSession


def live_response_counts(request):
    data = {}

    sessions = FeedbackSession.objects.all()

    for s in sessions:
        data[s.id] = {
            "responses": s.responses.count()
        }

    return JsonResponse(data)
    