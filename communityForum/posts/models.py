from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager




class Topic(models.Model):
    """ Topics contain posts """

    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def get_absolute_url(self):
        return reverse('topic-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return self.title



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



class Answer(models.Model):
    """ Comments are replies to posts """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    tags = TaggableManager()

    def __str__(self):
        return self.body




# class Question(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=datetime.now, blank=True)
#     tags = TaggableManager()
    
#     def __str__(self):
#         return self.title

#     @property
#     def count_answers(self):
#         return Answer.objects.filter(question=self).count()

#     def get_answers(self):
#         return Answer.objects.filter(question=self)




# class Answer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(default=datetime.now, blank=True)

#     def __str__(self):
#         return self.question
