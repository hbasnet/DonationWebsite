from  __future__ import unicode_literals #so that database read all the languages
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=150)
    short_txt = models.TextField()
    body_txt = models.TextField() #after click takes to the full items
    date = models.CharField(max_length=12)
    time = models.CharField(max_length=12,default='00:00')
    picname = models.TextField() #saving a pic is not enough also need to be deleted when the items post is deleted
    picurl = models.TextField(default='-')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    catname = models.CharField(max_length=50,default='-')
    catid = models.IntegerField(default=0)
    ocatid = models.IntegerField(default=0) #keep track of main category
    show = models.IntegerField(default=0)
    
    def __str__(self): #to show in the list of already made admin
        return self.name + " | " + str(self.pk) #if i had said about instead of name then it would've shown about text in admin main
    #if nothing is return then it will show as Main Object
