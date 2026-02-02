from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from instructor.models.question_models import FeedbackSession
from instructor.models.response_models import FeedbackResponse, Answer


def student_feedback(request, session_id):
    session = get_object_or_404(
        FeedbackSession,
        id=session_id,
        is_active=True
    )
    questions = session.questions.prefetch_related('options')

    if request.method == 'POST':
        response = FeedbackResponse.objects.create(session=session)

        for question in questions:
            field_name = f"question_{question.id}"

            if question.q_type == 'checkbox':
                values = request.POST.getlist(field_name)
                answer_text = ", ".join(values)
            else:
                answer_text = request.POST.get(field_name, '')

            Answer.objects.create(
                response=response,
                question=question,
                answer_text=answer_text
            )

        return HttpResponse(
            "<h2>Thank you! Your feedback has been submitted anonymously.</h2>"
        )

    return render(request, 'student/feedback_form.html', {
        'session': session,
        'questions': questions
    })
