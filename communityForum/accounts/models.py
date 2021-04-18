from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='assets/img/default-profile-img.jpg', blank=True, null=True, upload_to='profile-img/')

    def __str__(self):
        return f'{self.user.username} Profile'


class Question(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    question  = models.TextField()
    tags  = TaggableManager()
    slug = models.SlugField(unique=True, max_length=100)

class Answer(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField()
    answer = models.TextField()
    tags  = TaggableManager()
    slug = models.SlugField(unique=True, max_length=100)

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=100)
        
