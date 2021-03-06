from  __future__ import unicode_literals #so that database read all the languages
from django.db import models

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=50)
    count = models.IntegerField(default = 0) #this is required to keep count of category
    
    def __str__(self): #to show in the list of already made admin
        return self.name + " | " + str(self.pk) #if i had said about instead of name then it would've shown about text in admin main
    #if nothing is return then it will show as Main Object


