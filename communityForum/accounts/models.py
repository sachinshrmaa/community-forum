from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(default='default-profile.png', blank=True, null=True, upload_to='profile-img/')

    def __str__(self):
        return f'{self.user.username} Profile'
