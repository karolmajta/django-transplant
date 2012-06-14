from django.db import models
from django.contrib.auth.models import User

class OtherManager(models.Manager):
    pass

class TestModel(models.Model):
    objects = models.Manager()
    other_manager = OtherManager()

    user = models.ForeignKey(User)

class CustomUserFieldNameModel(models.Model):
    person = models.ForeignKey(User)