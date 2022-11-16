from django.db import models

from django.contrib.auth.models import User
from datetime import datetime, date


class Post(models.Model):
    text = models.CharField(max_length=200)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'


class Profile(models.Model):
    bio = models.CharField(max_length=200,blank=True )
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    content_type = models.CharField(max_length=50, blank=True)
    following = models.ManyToManyField(User, related_name="followers")

    def __str__(self):
        return 'id=' + str(self.id) + ',text="' + self.text + '"'
