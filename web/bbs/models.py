from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    allow_script = models.BooleanField()
    author = models.ForeignKey('auth.User')

    def __str__(self):
        return "Post '{}'".format(self.title)

class BoardUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    notarized = models.BooleanField()

    def __str__(self):
        return "BoardUser '{}' ({})".format(self.username,
                ['Normal', 'Notarized'][self.notarized])
