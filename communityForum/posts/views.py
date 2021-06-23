from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.db.models import Q


from .models import Question, Answer, Topic
from .forms import CreateCommentForm, CreateTopicForm





class FeedsListView(ListView):
    model = Question
    template_name = 'posts/feeds.html'
    

    def get_context_data(self, **kwargs):
        context = super(FeedsListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['posts'] = Question.objects.all().order_by('-timestamp')
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
    fields = ['title', 'body']
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


def search_view(request):
    query = request.GET.get('q')
    post = Question.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    context = {
        'search_obj' : post, 
    }
    return render(request, "posts/search.html", context)