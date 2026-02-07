import uuid
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from instructor.models.question_models import FeedbackSession
from instructor.models.response_models import FeedbackResponse, Answer
from instructor.models.attendance_models import SessionAttendance
from django.db import IntegrityError


# -------------------------------------------------
# DEVICE TOKEN (anonymous student identification)
# -------------------------------------------------
def get_device_token(request, session_id):
    key = f"device_token_{session_id}"

    if key not in request.session:
        request.session[key] = str(uuid.uuid4())

    return request.session[key]


# -------------------------------------------------
# PUBLIC QR PAGE  (MAIN STUDENT PAGE)
# -------------------------------------------------
def public_feedback(request, token):

    session = get_object_or_404(
        FeedbackSession,
        public_token=token,
        is_active=True
    )

    questions = session.questions.prefetch_related('options')

    # ----------------------------
    # SUBMIT FEEDBACK
    # ----------------------------
    if request.method == "POST":

        device_token = get_device_token(request, session.id)

        # Prevent duplicate voting
        if FeedbackResponse.objects.filter(
                session=session,
                device_token=device_token
        ).exists():
            return HttpResponse("You already submitted feedback.", status=403)

        # Do not allow submission if teacher not opened
        if not session.feedback_open:
            return HttpResponse("Feedback not yet allowed by teacher.", status=403)

        response = FeedbackResponse.objects.create(
            session=session,
            device_token=device_token
        )

        for question in questions:
            answer_text = request.POST.get(f"question_{question.id}", "")

            Answer.objects.create(
                response=response,
                question=question,
                answer_text=answer_text
            )

        return HttpResponse("Thank you! Feedback submitted successfully.")

    # ----------------------------
    # NORMAL PAGE LOAD
    # ----------------------------
    return render(
        request,
        "student/feedback_form.html",
        {
            "session": session,
            "questions": questions,
        }
    )


# -------------------------------------------------
# STUDENT PRESENCE CLICK
# -------------------------------------------------


def mark_attendance(request, token):
    """
    Student clicks: I AM PRESENT
    Creates anonymous presence using device token
    """

    session = get_object_or_404(
        FeedbackSession,
        public_token=token,
        is_active=True
    )

    device_token = request.session.session_key
    if not device_token:
        request.session.create()
        device_token = request.session.session_key

    # prevent duplicate presence
    SessionAttendance.objects.get_or_create(
        session=session,
        device_token=device_token
    )

    return JsonResponse({
        "success": True,
        "present_count": session.attendances.count()
    })

# -------------------------------------------------
# CHECK TEACHER PERMISSION (POLLING)
# -------------------------------------------------
def feedback_status(request, token):
    session = get_object_or_404(
        FeedbackSession,
        public_token=token,
        is_active=True
    )

    return JsonResponse({
        "open": session.feedback_open
    })

def student_feedback(request, session_id):
    from django.shortcuts import get_object_or_404, render
    from instructor.models.question_models import FeedbackSession

    session = get_object_or_404(FeedbackSession, id=session_id)

    
    return render(request, "instructor/feedback/student_feedback.html", {
        "session": session
    })


def submit_feedback(request, session_id):
    session = get_object_or_404(FeedbackSession, id=session_id)

    device_token = request.COOKIES.get("device_token")

    if not device_token:
        return render(request, "instructor/feedback/not_present.html")

    # 🚫 Already submitted?
    if FeedbackResponse.objects.filter(session=session, device_token=device_token).exists():
        return render(request, "instructor/feedback/already_submitted.html")

    # Save response
    try:
        response = FeedbackResponse.objects.create(
            session=session,
            device_token=device_token
        )
    except IntegrityError:
        return render(request, "instructor/feedback/already_submitted.html")

    # Save answers
    for q in session.questions.all():
        value = request.POST.get(f"question_{q.id}", "")

        Answer.objects.create(
            response=response,
            question=q,
            answer_text=value
        )

    return render(request, "instructor/feedback/thank_you.html")


