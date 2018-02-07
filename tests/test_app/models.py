from django.contrib.auth.models import User
from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=30)
    race = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
