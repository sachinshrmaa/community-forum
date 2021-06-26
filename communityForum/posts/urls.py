from django.urls import path

from .views import (
    TopicListView, TopicCreateView,
    TopicDetailView, PostCreateView,
    PostDetailView, PostUpdateView,
    PostDeleteView, FeedsListView, 
    search_view, answer_upvotes,
    answer_downvotes, tagged_posts
    )


urlpatterns = [
    path('', FeedsListView.as_view(), name="feeds"),
    path('topics/', TopicListView.as_view(), name="forum-index"),
    path('search/', search_view, name="search"),
    path('topics/add/', TopicCreateView.as_view(), name='topic-add'),
    path('tags/<slug>/', tagged_posts, name="tagged-article"),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('q/newpost/', PostCreateView.as_view(), name='post-create'),
    path('q/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('q/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('q/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('q/<int:pk>/upvote/', answer_upvotes, name ='up-vote'),
    path('q/<int:pk>/downvote/', answer_downvotes, name ='down-vote'),
]