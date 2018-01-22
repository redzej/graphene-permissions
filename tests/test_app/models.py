from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30)

    #class Meta:
    #    app_label = 'test_app'


class Pet(models.Model):
    name = models.CharField(max_length=30)
    race = models.CharField(max_length=30)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    #class Meta:
    #    app_label = 'test_app'
