from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden,  JsonResponse

from instructor.models.question_models import FeedbackSession, Question, Option
from instructor.models.teacher import Teacher

from instructor.forms import FeedbackSessionForm   # 👈 CLEAN IMPORT
from django.http import JsonResponse
from django.db.models import Count, Avg, FloatField
from django.db.models.functions import Cast

import uuid
import qrcode
import base64
from io import BytesIO

from django.utils import timezone
from django.urls import reverse

from instructor.models.response_models import Answer



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
    

from instructor.models.question_models import FeedbackSession


def live_response_counts(request):
    data = {}

    sessions = FeedbackSession.objects.all()

    for s in sessions:
        data[s.id] = {
            "responses": s.responses.count()
        }

    return JsonResponse(data)


def session_report(request, session_id):

    session = get_object_or_404(FeedbackSession, id=session_id)

    # ---------- FETCH TEACHER PROFILE ----------
    teacher_profile = getattr(session.teacher, "teacher_profile", None)

    teacher_name = "Unknown"
    department_name = "Not Assigned"

    if teacher_profile:
        teacher_name = teacher_profile.first_name or session.teacher.username

        if teacher_profile.department:
            department_name = teacher_profile.department.name
        elif teacher_profile.dept_name:
            department_name = teacher_profile.dept_name

    # ------------------------------------------

    report = []

    for q in session.questions.prefetch_related("options"):

        answers = Answer.objects.filter(question=q)

        # ---------------- TEXT ----------------
        if q.q_type in ["text", "textarea"]:
            report.append({
                "question": q,
                "type": "text",
                "comments": answers.exclude(answer_text="")[:100]
            })

        # ---------------- RATING ----------------
        elif q.q_type == "rating":
            avg = answers.exclude(answer_text="").annotate(
                num=Cast("answer_text", FloatField())
            ).aggregate(avg=Avg("num"))["avg"] or 0

            report.append({
                "question": q,
                "type": "rating",
                "average": round(avg, 2),
                "total": answers.count()
            })

        # ---------------- CHECKBOX ----------------
        elif q.q_type == "checkbox":
            counter = {}

            for ans in answers:
                if ans.answer_text:
                    selected = ans.answer_text.split(",")
                    for opt_id in selected:
                        counter[opt_id] = counter.get(opt_id, 0) + 1

            option_data = []
            total = answers.count()

            for opt in q.options.all():
                count = counter.get(str(opt.id), 0)
                percent = (count / total * 100) if total else 0

                option_data.append({
                    "label": opt.text,
                    "count": count,
                    "percent": round(percent, 1)
                })

            report.append({
                "question": q,
                "type": "choice",
                "options": option_data,
                "total": total
            })

        # ---------------- RADIO / YESNO ----------------
        else:
            option_data = []
            total = answers.count()

            for opt in q.options.all():
                count = answers.filter(answer_text=str(opt.id)).count()
                percent = (count / total * 100) if total else 0

                option_data.append({
                    "label": opt.text,
                    "count": count,
                    "percent": round(percent, 1)
                })

            report.append({
                "question": q,
                "type": "choice",
                "options": option_data,
                "total": total
            })

    return render(request, "instructor/report.html", {
        "session": session,
        "report": report,
        "teacher_name": teacher_name,
        "department_name": department_name,
    })
