from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    age = models.PositiveIntegerField(null=True,blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    is_developer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'user'

    

