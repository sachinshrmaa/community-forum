from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from collections import Counter




class Vote(models.Model):
    """Model class to host every vote, made with ContentType framework to
    allow a single model connected to Questions and Answers."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    value = models.BooleanField(default=True)
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        related_name="votes_on",
        on_delete=models.CASCADE,
    )
    object_id = models.CharField(max_length=50, blank=True, null=True)
    vote = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Vote")
        verbose_name_plural = _("Votes")
        index_together = ("content_type", "object_id")
        unique_together = ("user", "content_type", "object_id")



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
    votes = GenericRelation(Vote)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    @property
    def count_answers(self):
        return Answer.objects.filter(post=self).count()

    def count_votes(self):
        """Method to update the sum of the total votes. Uses this complex query
        to avoid race conditions at database level."""
        dic = Counter(self.votes.values_list("value", flat=True))
        Question.objects.filter(id=self.id).update(total_votes=dic[True] - dic[False])
        self.refresh_from_db()

    def get_upvoters(self):
        """Returns a list containing the users who upvoted the instance."""
        return [vote.user for vote in self.votes.filter(value=True)]

    def count_upvotes(self):
        return self.votes.filter(value=True).count()

    def get_downvoters(self):
        """Returns a list containing the users who downvoted the instance."""
        return [vote.user for vote in self.votes.filter(value=False)]

    def count_downvotes(self):
        return self.votes.filter(value=False).count()

class Answer(models.Model):
    """ Comments are replies to posts """

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    tags = TaggableManager()

    def __str__(self):
        return self.body


