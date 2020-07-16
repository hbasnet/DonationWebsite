from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from items.models import Items

@login_required
def mylist(request):
    posted_items = {
        'items': Items.objects.all().filter(owner__username=request.user)
    }
    return render(request,'front/mylist.html',posted_items)

def profile(request):
    
    return render(request,'front/profile.html')