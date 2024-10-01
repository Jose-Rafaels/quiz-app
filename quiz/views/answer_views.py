from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ..services.AnswerService import AnswerService
from ..models import QuizAttempt
from django.shortcuts import get_object_or_404


@csrf_exempt
@login_required
def save_answer(request):
    if request.method == "POST":
        try:
            attempt_id = request.POST.get("attempt_id")
            question_id = request.POST.get("question_id")
            choice_id = request.POST.get("choice_id")

            attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

            # Panggil service untuk menyimpan jawaban
            AnswerService.save_answer(attempt, question_id, choice_id)
            
            return JsonResponse(
                {"status": "success", "message": "Answer saved successfully!"}
            )

        except QuizAttempt.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Quiz attempt not found."}
            )
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "An error occurred while saving the answer.",
                }
            )

    return JsonResponse({"status": "error", "message": "Invalid request."})
