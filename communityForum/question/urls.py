from django.urls import path
from .views import QuestionListView, QuestionAnsListView, QuestionDetailView, CreateQuestionView

urlpatterns = [
    path('feeds/', QuestionListView.as_view(), name="index_list"),
    path('answered/', QuestionAnsListView.as_view()),
    path('q/<slug>/', QuestionDetailView.as_view()),

    path('q/create', CreateQuestionView.as_view(), name="create-question"),
]