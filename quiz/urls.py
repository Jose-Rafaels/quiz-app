from django.urls import path
from .views import quiz_views, answer_views, quiz_attempt_views, auth_views

urlpatterns = [
    path("", auth_views.dashboard, name="dashboard"),
    path("create-quiz/", quiz_views.create_quiz, name="create_quiz"),
    path(
        "<int:attempt_id>/question/",
        quiz_views.quiz_question,
        name="quiz_question",
    ),
    path(
        "<int:quiz_id>/start/",
        quiz_attempt_views.start_quiz_attempt,
        name="start_quiz_attempt",
    ),
    path("save-answer/", answer_views.save_answer, name="save_answer"),
    path(
        "<int:attempt_id>/result",
        quiz_attempt_views.quiz_result,
        name="quiz_result",
    ),
    path(
        "<int:attempt_id>/finish/",
        quiz_attempt_views.finish_quiz,
        name="finish_quiz",
    ),
    path("my-quizzes/", quiz_views.my_quizzes, name="my_quizzes"),
    path("result/", quiz_attempt_views.quiz_results, name="quiz_results"),
    path(
        "admin/quiz-attempts/",
        quiz_attempt_views.admin_quiz_attempts,
        name="admin_quiz_attempts",
    ),
    path('admin/user-scores/', quiz_attempt_views.admin_view_user_scores, name='admin_user_scores'),
    path("admin/quizzes/", quiz_attempt_views.admin_quizzes, name="admin_quizzes"),
    path('admin/<int:quiz_id>/questions/', quiz_views.list_quiz, name='list_question'),
]
