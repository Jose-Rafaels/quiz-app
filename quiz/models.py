from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # Admin sebagai pembuat kuis
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, related_name="questions"
    )  # Pertanyaan terkait dengan kuis
    question_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )  # Pilihan terkait dengan pertanyaan
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(
        default=False
    )  # Menandai apakah pilihan ini benar atau salah
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.choice_text


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='quizattempt'
    )  # Pengguna yang mencoba kuis
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE
    )  # Kuis yang sedang dikerjakan
    score = models.FloatField(default=0)  # Skor akhir kuis
    start_time = models.DateTimeField(
        auto_now_add=True
    )  # Waktu ketika pengguna memulai kuis
    end_time = models.DateTimeField(
        null=True, blank=True
    )  # Waktu ketika pengguna menyelesaikan kuis, bisa null jika belum selesai

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"


class Answer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt, on_delete=models.CASCADE
    )  # Kaitan dengan usaha kuis
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE
    )  # Pertanyaan yang dijawab
    choice = models.ForeignKey(
        Choice, on_delete=models.CASCADE
    )  # Jawaban yang dipilih oleh pengguna
    is_correct = models.BooleanField(default=False)  # Menandai apakah jawaban ini benar
    answered_at = models.DateTimeField(auto_now_add=True)  # Waktu pengguna menjawab

    def __str__(self):
        return f"Answer by {self.attempt.user.username} on {self.question}"
