from django.db import models
from django.contrib.auth.models import User

class TestModel(models.Model):
    user = models.ForeignKey(User)

class CustomUserFieldNameModel(models.Model):
    person = models.ForeignKey(User)