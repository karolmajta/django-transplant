from django.db import models
from django.contrib.auth.models import User

class OtherManager(models.Manager):
    pass

class TestModel(models.Model):
    objects = models.Manager()
    other_manager = OtherManager()

    user = models.ForeignKey(User)
    was_saved = models.BooleanField(default=False)
    
    def save(self, force_insert=False, force_update=False, using=None):
        self.was_saved = True if self.pk is not None else False
        super(TestModel, self).save(force_insert=force_insert, force_update=force_update, using=using)
        

class CustomUserFieldNameModel(models.Model):
    person = models.ForeignKey(User)