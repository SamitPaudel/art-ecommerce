from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

# Create your models here.
from pages import render

from accounts.models import Account

class Artist(models.Model):
    artist_email = models.ForeignKey(Account, on_delete=models.CASCADE)
    artist_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=500)
    description = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return self.artist_name
