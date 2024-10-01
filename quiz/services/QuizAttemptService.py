from django.utils import timezone
from django.shortcuts import get_object_or_404
from ..models import QuizAttempt, Answer, Quiz


class QuizAttemptService:

    @staticmethod
    def create_quiz_attempt(user, quiz_id):

        try:
            # Ambil instance Quiz berdasarkan quiz_id
            quiz = get_object_or_404(Quiz, id=quiz_id)

            # Buat instance QuizAttempt baru
            quiz_attempt = QuizAttempt.objects.create(
                user=user,
                quiz=quiz,  # Assign instance Quiz, bukan ID
                start_time=timezone.now(),
                score=0,  # Skor awal default adalah 0
            )
            return quiz_attempt
        except Exception as e:
            print(f"Error creating quiz attempt: {e}")
            raise

    @staticmethod
    def calculate_final_score(quiz_attempt):

        try:
            total_questions = quiz_attempt.quiz.question_set.count()
            correct_answers = Answer.objects.filter(
                attempt=quiz_attempt, is_correct=True
            ).count()

            if total_questions == 0:
                return 0

            final_score = (correct_answers / total_questions) * 100
            return final_score
        except Exception as e:
            print(f"Error calculating final score: {e}")
            raise

    @staticmethod
    def finish_quiz_attempt(quiz_attempt):
        try:
            final_score = QuizAttemptService.calculate_final_score(quiz_attempt)

            quiz_attempt.score = final_score
            quiz_attempt.end_time = timezone.now()
            quiz_attempt.save()

            return quiz_attempt
        except Exception as e:
            print(f"Error finishing quiz attempt: {e}")
            raise

    @staticmethod
    def get_completed_quizzes(user):

        try:
            completed_quizzes = QuizAttempt.objects.filter(
                user=user, end_time__isnull=False
            )
            return completed_quizzes
        except Exception as e:
            print(f"Error fetching completed quizzes: {e}")
            raise

    @staticmethod
    def get_quiz_result(attempt_id, user):

        try:
            # Dapatkan QuizAttempt dan validasi bahwa ini milik user
            quiz_attempt = QuizAttempt.objects.get(id=attempt_id, user=user)

            # Pastikan bahwa kuis telah selesai (end_time tidak null)
            if not quiz_attempt.end_time:
                raise ValueError("Quiz has not been completed yet.")

            # Ambil pembuat kuis
            quiz_creator = quiz_attempt.quiz.created_by.username

            # Siapkan hasil kuis dalam bentuk dictionary
            result = {
                "quiz_title": quiz_attempt.quiz.title,
                "score": quiz_attempt.score,
                "start_time": quiz_attempt.start_time,
                "end_time": quiz_attempt.end_time,
                "quiz_creator": quiz_creator,
            }

            return result
        except QuizAttempt.DoesNotExist:
            raise ValueError("QuizAttempt not found or you don't have permission.")
        except Exception as e:
            print(f"Error retrieving quiz result: {e}")
            raise

    @staticmethod
    def get_quiz_attempts_by_created(admin_user):
        try:
            quizzes = Quiz.objects.filter(created_by=admin_user)
            return QuizAttempt.objects.all().filter(quiz__in=quizzes)

        except Exception as e:
            print(f"Error fetching quiz attempts: {e}")
            raise

    @staticmethod
    def get_quizzes_by_created(admin_user):
        try:
            return Quiz.objects.filter(created_by=admin_user)
        except Exception as e:
            print(f"Error fetching quizzes: {e}")
            raise
        
    @staticmethod
    def get_user_attempts_for_admin(admin_user):
        """
        Mengambil semua attempt (nilai) dari kuis yang dibuat oleh admin.
        """
        # Mengambil semua kuis yang dibuat oleh admin
        quizzes = Quiz.objects.filter(created_by=admin_user)

        # Mengambil semua attempt dari kuis yang dibuat oleh admin
        attempts = QuizAttempt.objects.filter(quiz__in=quizzes).select_related('user', 'quiz')

        return attempts 