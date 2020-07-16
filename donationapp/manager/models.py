from  __future__ import unicode_literals #so that database read all the languages
from django.db import models

# Create your models here.
class Manager(models.Model):
    name = models.CharField(max_length=30)
    utxt = models.TextField()
    email = models.TextField(default = "")
    
    def __str__(self): #to show in the list of already made admin
        return self.name
