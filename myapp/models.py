from django.db import models

# Create your models here.

class GitUser(models.Model):
    githubuser = models.CharField(max_length=1000)
    githubuserimage = models.CharField(max_length=1000)
    username = models.CharField(max_length=1000)

    def __str__(self):
        return self.githubuser