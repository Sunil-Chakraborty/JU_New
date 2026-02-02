from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from instructor.models.question_models import FeedbackSession, Question, Option
from instructor.forms.question_forms import QuestionForm


@login_required
def create_question(request, session_id):
    session = get_object_or_404(FeedbackSession, id=session_id)

    if session.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.session = session
            question.save()

            for opt in request.POST.getlist("options[]"):
                if opt.strip():
                    Option.objects.create(question=question, text=opt.strip())

            return redirect("instructor:create_question", session_id=session.id)
    else:
        form = QuestionForm()

    questions = session.questions.prefetch_related("options")

    return render(
        request,
        "instructor/create_question.html",
        {
            "form": form,
            "session": session,
            "questions": questions,
        },
    )


@login_required
def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if question.session.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()

            # Replace options
            question.options.all().delete()
            for opt in request.POST.getlist("options[]"):
                if opt.strip():
                    Option.objects.create(question=question, text=opt.strip())

            return redirect(
                "instructor:create_question",
                session_id=question.session.id
            )
    else:
        form = QuestionForm(instance=question)

    return render(
        request,
        "instructor/edit_question.html",
        {
            "form": form,
            "question": question,
        },
    )


@login_required
def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if question.session.teacher != request.user:
        return HttpResponseForbidden("Not allowed")

    session_id = question.session.id
    question.delete()

    return redirect("instructor:create_question", session_id=session_id)
