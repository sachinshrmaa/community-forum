from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from collections import Counter


class Topic(models.Model):
    """ Topics contain posts """

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title

    @property
    def count_questions(self):
        return Question.objects.filter(topic=self).count()



class Question(models.Model):
    """ Posts can be found under its topic. """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=50, default='untitled')
    body = models.TextField()
    tags = TaggableManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def count_answers(self):
        return Answer.objects.filter(post=self).count()

   



class Answer(models.Model):
    """ Comments are replies to posts """
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    tags = TaggableManager()
    up_votes = models.ManyToManyField(User, related_name="up_vote")
    down_votes = models.ManyToManyField(User, related_name="down_vote")

    def total_up_votes(self):
        return self.up_votes.count()

    def total_down_votes(self):
        return self.down_votes.count()

    def __str__(self):
        return self.body

   

