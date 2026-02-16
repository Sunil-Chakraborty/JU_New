from collections import defaultdict
from instructor.models.teacher import Teacher
from instructor.models.question_models import FeedbackSession
from instructor.models.response_models import FeedbackResponse, Answer



from django.db.models import Avg, FloatField
from django.db.models.functions import Cast



def build_report_data(session):

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

    return report
