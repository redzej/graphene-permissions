from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Pet(models.Model):
    name = models.CharField(max_length=30)
    race = models.CharField(max_length=30)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
