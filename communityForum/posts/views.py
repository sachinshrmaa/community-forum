
from django.shortcuts import render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Question, Answer, Topic
from .forms import CreateCommentForm, CreateTopicForm



class FeedsListView(ListView):
    model = Question
    template_name = 'posts/feeds.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(FeedsListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context



class TopicListView(ListView):
    model = Topic
    template_name = 'posts/index.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'topics'


class TopicDetailView(DetailView):
    model = Topic

    def get_context_data(self, **kwargs):
        context = super(TopicDetailView, self).get_context_data(**kwargs)
        context['posts'] = Question.objects.filter(topic=self.kwargs.get('pk'))
        return context


class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    fields = ['title', 'description']
    success_url = '/topics'

    def form_valid(self, form):
        return super().form_valid(form)



# Post views

class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Question
    form_class = CreateCommentForm
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Answer.objects.filter(post=self.kwargs.get('pk'))
        context['form'] = CreateCommentForm(initial={'post': self.object, 'author': self.request.user})

        return context

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(PostDetailView, self).form_valid(form)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ['title', 'body', 'topic', 'tags']
    template_name = 'posts/post_form.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title', 'body', 'topic', 'tags']
    template_name = 'posts/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    success_url = '/'
    template_name = 'posts/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    



