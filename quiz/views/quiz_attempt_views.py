from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from ..services.QuizAttemptService import QuizAttemptService
from ..models import Quiz, QuizAttempt


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    try:
        # Panggil service untuk membuat QuizAttempt baru
        quiz_attempt = QuizAttemptService.create_quiz_attempt(request.user, quiz)
        return redirect("quiz_question", attempt_id=quiz_attempt.id)
    except Exception as e:
        print(f"Error: {e}")
        return render(
            request, "error_page.html", {"message": "Unable to start the quiz."}
        )


@login_required
def finish_quiz(request, attempt_id):
    try:
        quiz_attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=request.user)

        # Panggil service untuk menyelesaikan quiz_attempt (menghitung skor dan mengisi end_time)
        QuizAttemptService.finish_quiz_attempt(quiz_attempt)

        return redirect("quiz_result", attempt_id=attempt_id)
    except Exception as e:
        print(f"Error: {e}")
        return render(
            request, "error_page.html", {"message": "Unable to finish the quiz."}
        )


@login_required
def start_quiz_attempt(request, quiz_id):
    try:
        # Panggil service untuk membuat QuizAttempt baru berdasarkan quiz_id
        quiz_attempt = QuizAttemptService.create_quiz_attempt(request.user, quiz_id)

        # Redirect ke halaman pertanyaan pertama
        return redirect("quiz_question", attempt_id=quiz_attempt.id)
    except Exception as e:
        print(f"Error: {e}")
        return render(
            request, "error_page.html", {"message": "Unable to start the quiz."}
        )


@login_required
def quiz_result(request, attempt_id):
    try:
        # Ambil hasil kuis menggunakan service
        result = QuizAttemptService.get_quiz_result(attempt_id, request.user)
        error_message = request.GET.get("error")

        # Render hasil ke template, dengan pesan error jika ada
        return render(
            request,
            "quiz_result.html",
            {"result": result, "error_message": error_message},
        )

    except ValueError as e:
        return render(request, "error_page.html", {"message": str(e)})
    except Exception as e:
        print(f"Error: {e}")
        return render(
            request,
            "error_page.html",
            {"message": "An error occurred while retrieving the quiz result."},
        )


@login_required
def quiz_results(request):
    try:
        # Panggil service untuk mengambil hasil kuis yang telah diselesaikan oleh user
        completed_quizzes = QuizAttemptService.get_completed_quizzes(request.user)
        context = {"completed_quizzes": completed_quizzes}
        return render(request, "quiz_results.html", context)
    except Exception as e:
        print(f"Error: {e}")
        return render(
            request, "error_page.html", {"message": "Unable to retrieve quiz results."}
        )


@admin_required
def admin_quiz_attempts(request):
    try:
        attempts = QuizAttemptService.get_quiz_attempts_by_created(request.user)

        context = {"attempts": attempts}
        return render(request, "admin/quiz_attempts.html", context)

    except Exception as e:
        print(f"Error: {e}")
        return render(
            request, "error_page.html", {"message": "Unable to retrieve quiz attempts."}
        )


@admin_required
def admin_view_user_scores(request):
    # Mengambil semua attempt dari kuis yang dibuat oleh admin
    user_attempts = QuizAttemptService.get_user_attempts_for_admin(request.user)
    
    return render(request, 'admin/user_scores.html', {'user_attempts': user_attempts})

@admin_required
def admin_quizzes(request):
    try:
        # Panggil service untuk mengambil semua kuis yang dibuat oleh admin
        quizzes = QuizAttemptService.get_quizzes_by_created(request.user)
        return render(request, "admin/quizzes.html", {"quizzes": quizzes})

    except Exception as e:
        print(f"Error: {e}")
        return render(
            request, "error_page.html", {"message": "Unable to retrieve quizzes."}
        )
