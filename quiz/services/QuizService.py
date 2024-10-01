from ..models import Quiz, Choice, Question, QuizAttempt
from django.shortcuts import get_object_or_404


class QuizService:

    @staticmethod
    def get_quizzes_by_user(user_id):
        return Quiz.objects.filter(created_by_id=user_id)

    @staticmethod
    def get_quizzes_for_user(user):
        """
        Mengambil semua kuis yang telah dikerjakan oleh user.
        """
        return Quiz.objects.filter(attempt__user=user).distinct()
    @staticmethod
    def get_all_quizzes():
        return Quiz.objects.all()
    
    @staticmethod
    def get_quiz_by_id(quiz_id, user):
        return get_object_or_404(Quiz, id=quiz_id, created_by=user)


    @staticmethod
    def create_quiz(user, title, description, questions_data):
        try:
            # Buat objek kuis
            quiz = Quiz.objects.create(
                title=title,
                description=description,
                created_by=user,
                total_questions=len(questions_data),
            )

            # Iterasi melalui data pertanyaan dan pilihan
            for question_data in questions_data:
                question_text = question_data["question_text"]
                choices_data = question_data["choices"]
                correct_choice_index = question_data["correct_choice"]

                # Buat pertanyaan
                question = Question.objects.create(
                    quiz=quiz, question_text=question_text
                )

                # Buat pilihan untuk pertanyaan
                for i, choice_text in enumerate(choices_data):
                    is_correct = i == correct_choice_index
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text,
                        is_correct=is_correct,
                    )
            return quiz
        except Exception as e:
            # Tangani error dan lempar exception jika perlu
            print(f"Error creating quiz: {e}")
            raise

    @staticmethod
    def get_question(user, attempt_id, question_number):
        try:
            # Dapatkan QuizAttempt milik user
            attempt = get_object_or_404(QuizAttempt, id=attempt_id, user=user)

            # Ambil semua pertanyaan dari kuis
            questions = attempt.quiz.question_set.all()
            total_questions = questions.count()

            # Validasi nomor pertanyaan
            if 0 <= question_number < total_questions:
                current_question = questions[question_number]
                return current_question, total_questions, attempt

            # Jika nomor pertanyaan tidak valid
            return None, total_questions, attempt

        except Exception as e:
            print(f"Error fetching question: {e}")
            raise
