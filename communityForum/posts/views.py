from django.shortcuts import render

from .models import Question



def home_feeds(request):
    posts = Question.objects.all().order_by('-timestamp')
    context = {
        'posts' : posts
    }
    return render(request, 'posts/feeds.html', context )




def question_detail(request, pk):
    post = Question.objects.get(id=pk)
    context = {
        'post': post,
    }

    return render(request, "posts/post_detail.html", context)
