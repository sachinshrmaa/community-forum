from django.shortcuts import render, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormMixin
from django.views.generic import (ListView, DetailView,
    CreateView, UpdateView, DeleteView
)
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer, Topic
from .forms import CreateCommentForm, CreateTopicForm
from taggit.models import Tag
from django.db.models import Count




class FeedsListView(ListView):
    model = Question
    template_name = 'posts/feeds.html'

    

    def get_context_data(self, **kwargs):
        context = super(FeedsListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        context['posts'] = Question.objects.all().order_by('-timestamp')
        context["common_tags"] = Question.tags.most_common()

        return context


class TopicListView(ListView):
    model = Topic
    template_name = 'posts/index.html'  
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
    login_url = '/login/'

    def form_valid(self, form):
        return super().form_valid(form)


class PostDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Question
    form_class = CreateCommentForm
    template_name = 'posts/post_detail.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['comments'] = Answer.objects.annotate(votes =Count('up_votes')).order_by('-votes').filter(post=self.kwargs.get('pk'))
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
    login_url = '/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        # form.instance.topic = Topic.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    fields = ['title', 'body', 'topic', 'tags']
    template_name = 'posts/post_form.html'
    login_url = '/login/'

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
    login_url = '/login/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False    


@login_required(login_url='/login')
def search_view(request):
    query = request.GET.get('q')
    post = Question.objects.filter(Q(title__icontains=query) | Q(body__icontains=query))

    context = {
        'search_obj' : post, 
    }
    return render(request, "posts/search.html", context)


@login_required(login_url='/login')
def answer_upvotes(request, pk):
    answer = get_object_or_404(Answer, id=request.POST.get('up_vote'))

    if answer.up_votes.filter(id=request.user.id).exists() :
        answer.up_votes.remove(request.user)
    else:
        answer.up_votes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))


@login_required(login_url='/login')
def answer_downvotes(request, pk):
    answer = get_object_or_404(Answer, id=request.POST.get('down_vote'))

    if answer.down_votes.filter(id=request.user.id).exists() :
        answer.down_votes.remove(request.user)
    else:
        answer.down_votes.add(request.user)

    return HttpResponseRedirect(reverse('post-detail', args=[str(pk)]))



def tagged_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    question = Question.objects.filter(tags=tag)
    common_tags = Question.tags.most_common()
    context = {
        'tag':tag,
        'posts': question,
        'common_tags' : common_tags,
    }
    return render(request, 'posts/tags.html', context)