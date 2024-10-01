from django.shortcuts import get_object_or_404
from ..models import Choice, Question, Answer, Quiz


class AnswerService:

    @staticmethod
    def get_quiz_answers(quiz_id):
        """
        Mengambil semua pertanyaan dan jawaban terkait dari suatu kuis tertentu.
        """
        try:
            # Dapatkan kuis berdasarkan ID
            quiz = Quiz.objects.get(id=quiz_id)

            # Dapatkan semua pertanyaan yang terkait dengan kuis
            questions = quiz.questions.all()  # Pastikan ada related_name='questions' pada model Question

            # Siapkan struktur data untuk pertanyaan dan jawaban
            quiz_answers = []
            for question in questions:
                # Ambil semua pilihan jawaban yang terkait dengan pertanyaan ini
                answers = question.choice_set.all()
                quiz_answers.append({
                    'question': question,
                    'answers': answers
                })

            return quiz_answers

        except Quiz.DoesNotExist:
            return None  # Kuis tidak ditemukancmethod
    def get_saved_answer(attempt, question):

        try:
            saved_answer = Answer.objects.filter(
                attempt=attempt, question=question
            ).first()
            return saved_answer.choice.id if saved_answer else None
        except Exception as e:
            print(f"Error fetching saved answer: {e}")
            raise

    @staticmethod
    def save_answer(attempt, question_id, choice_id):
        try:
            question = get_object_or_404(Question, id=question_id)
            choice = get_object_or_404(Choice, id=choice_id)

            answer, created = attempt.answer_set.update_or_create(
                question=question,
                defaults={"choice": choice, "is_correct": choice.is_correct},
            )
            return answer
        except Exception as e:
            # Log error
            print(f"Error saving answer: {e}")
            raise
