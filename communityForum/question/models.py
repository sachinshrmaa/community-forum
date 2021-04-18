from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Question(models.Model):
    question = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    tags  = TaggableManager()

    '''
    Todo 
    - add auto slugify 
    - link answer and category model with the question model
    - votes
    '''


class Answer(models.Model):
    answer = models.TextField()
    slug = models.SlugField(unique=True, max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    tags  = TaggableManager()


class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
        
