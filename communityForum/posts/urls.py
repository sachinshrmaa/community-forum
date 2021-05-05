from django.urls import path

from .views import home_feeds, question_detail

urlpatterns = [
    path('q/<int:pk>/', question_detail, name="question-detail"),
    path('feeds/', home_feeds, name="feeds")
]