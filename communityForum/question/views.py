from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView

from .models import Question, Answer
from .forms import QuestionForm



class QuestionsIndexListView(LoginRequiredMixin, ListView):
    """CBV to render a list view with all the registered questions."""

    model = Question
    paginate_by = 20
    context_object_name = "questions"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["popular_tags"] = Question.objects.get_counted_tags()
        context["active"] = "all"
        return context


class QuestionAnsListView(QuestionsIndexListView):
    """CBV to render a list view with all question which have been already
    marked as answered."""

    def get_queryset(self, **kwargs):
        return Question.objects.get_answered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "answered"
        return context


class QuestionListView(QuestionsIndexListView):
    """CBV to render a list view with all question which haven't been marked
    as answered."""
    
    def get_queryset(self, **kwargs):
        return Question.objects.get_unanswered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "unanswered"
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """View to call a given Question object and to render all the details about
    that Question."""

    model = Question
    context_object_name = "question"
    template_name = "question/question_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        question = self.get_object()
        if self.request.user.username == question.user.username:
            is_question_owner = True
        else:
            is_question_owner = False
        context["is_question_owner"] = is_question_owner
        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    View to handle the creation of a new question
    """
    form_class = QuestionForm
    template_name = "question/question_form.html"
    message = _("Your question has been created.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("question:index_list")