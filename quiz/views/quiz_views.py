from django.shortcuts import render, redirect
from ..services.QuizService import QuizService
from ..services.AnswerService import AnswerService
from django.contrib.auth.decorators import login_required
from ..decorators import admin_required
from django.core.exceptions import PermissionDenied


@admin_required
def my_quizzes(request):
    try:
        quizzes = QuizService.get_quizzes_by_admin(request.user)
        return render(request, "my_quizzes.html", {"quizzes": quizzes})
    except PermissionDenied:
        return render(
            request,
            "error_page.html",
            {"message": "You do not have permission to view this page"},
        )
    except Exception as e:
        # Log the error
        print(f"Error: {e}")
        return render(
            request,
            "error_page.html",
            {"message": "An error occurred while loading the quizzes"},
        )


# @login_required
# def quiz_question(request, attempt_id):
#     try:
#         # Dapatkan QuizAttempt
#         question_number = int(request.GET.get("question", 1)) - 1

#         # Panggil service untuk mendapatkan pertanyaan, total pertanyaan, dan attempt
#         current_question, total_questions, attempt = QuizService.get_question(
#             request.user, attempt_id, question_number
#         )

#         if current_question is None:
#             # Jika pertanyaan tidak valid, kembalikan ke halaman yang sama
#             return redirect("quiz_question", attempt_id=attempt.id)

#         # Panggil service untuk mendapatkan jawaban yang disimpan
#         saved_choice = AnswerService.get_saved_answer(attempt, current_question)

#         # Siapkan context untuk template
#         context = {
#             "current_question": current_question,
#             "question_number": question_number + 1,
#             "total_questions": total_questions,
#             "saved_choice": saved_choice,
#             "attempt_id": attempt.id,
#         }

#         return render(request, "quiz_question.html", context)

#     except Exception as e:
#         print(f"Error: {e}")
#         return render(
#             request,
#             "error_page.html",
#             {"message": "An error occurred while fetching the question."},
#         )


@login_required
def quiz_question(request, attempt_id):
    try:
        # Dapatkan nomor pertanyaan dari query parameter, default ke 1 jika tidak ada
        question_number = int(request.GET.get("question", 1)) - 1

        # Panggil service untuk mendapatkan pertanyaan dan total pertanyaan
        current_question, total_questions, attempt = QuizService.get_question(
            request.user, attempt_id, question_number
        )
        if attempt.end_time is not None:
            # Jika kuis sudah selesai, redirect ke halaman hasil dengan pesan error
            return redirect(
                "quiz_result", attempt_id=attempt.id, error="Quiz telah selesai."
            )
        if current_question is None:
            # Jika pertanyaan tidak valid, redirect kembali
            return redirect("quiz_question", attempt_id=attempt.id)

        # Panggil service untuk mendapatkan jawaban yang disimpan
        saved_choice = AnswerService.get_saved_answer(attempt, current_question)
    
        # Dapatkan semua pertanyaan untuk navigasi nomor
        questions = attempt.quiz.question_set.all()
        question_status = []
        for question in questions:
            is_answered = attempt.answer_set.filter(question=question).exists()
            question_status.append({"question": question, "is_answered": is_answered})
        # Siapkan context untuk template
        context = {
            "current_question": current_question,
            "question_number": question_number + 1,
            "total_questions": total_questions,
            "saved_choice": saved_choice,
            "attempt_id": attempt.id,
            "questions": questions,  # Kirim semua pertanyaan untuk navigasi
            "question_status": question_status,
        }
        # print(f"Saved choice: {saved_choice}")
        # print(f"Current question: {current_question}")

        return render(request, "quiz_question.html", context)

    except Exception as e:
        print(f"Error: {e}")
        return render(
            request,
            "error_page.html",
            {"message": "An error occurred while fetching the question."},
        )


@admin_required
def create_quiz(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        # Ambil data pertanyaan dan pilihan dari POST
        questions_data = []
        questions = request.POST.getlist("questions[]")

        for i, question_text in enumerate(questions):
            choices = request.POST.getlist(f"choices[{i}][]")
            correct_choice = int(request.POST.get(f"correct_choice[{i}]"))

            questions_data.append(
                {
                    "question_text": question_text,
                    "choices": choices,
                    "correct_choice": correct_choice,
                }
            )

        # Panggil service untuk membuat kuis
        try:
            QuizService.create_quiz(request.user, title, description, questions_data)
            return redirect(
                "dashboard"
            )  # Setelah berhasil membuat kuis, kembali ke dashboard
        except Exception as e:
            # Jika ada error, kembalikan user ke halaman form dengan pesan error
            return render(
                request,
                "create_quiz.html",
                {
                    "error": "An error occurred while creating the quiz.",
                    "title": title,
                    "description": description,
                },
            )

    return render(request, "create_quiz.html")

@admin_required
def list_quiz(request, quiz_id):
    # Menggunakan service untuk mendapatkan kuis
    quiz = QuizService.get_quiz_by_id(quiz_id, request.user)
    
    # Menggunakan service untuk mendapatkan pertanyaan
    # questions_answer = QuizService.get_questions_for_quiz(quiz)
    questions_answer = AnswerService.get_quiz_answers(quiz_id)

    return render(request, 'list_question.html', {'quiz': quiz, 'quiz_answers': questions_answer})