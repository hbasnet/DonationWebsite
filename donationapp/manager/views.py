from django.shortcuts import render, get_object_or_404, redirect
from .models import Manager
from items.models import Items
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group, Permission


def manager_list(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    #permission check start.. divided between admin and normal user
    #this has to be done in both view and template because if someone remember the url the ??
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    #permission check end

    manager = Manager.objects.all()

    return render(request, 'back/manager_list.html', {'manager': manager})


def manager_del(request, pk):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    manager = Manager.objects.get(pk=pk)
    b = User.objects.filter(username=manager.utxt)
    b.delete()
    manager.delete()
    return redirect('manager_list')


def manager_group(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    group = Group.objects.all().exclude(name="masteruser")

    return render(request, 'back/manager_group.html', {'group': group})


def manager_group_add(request):

    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    if request.method == 'POST':
        name = request.POST.get('name')

    if name != "":

        if len(Group.objects.filter(name=name)) == 0:  # if it already exists then don't create
            group = Group(name=name)
            group.save()

    return redirect('manager_group')


def manager_group_del(request, name):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    b = Group.objects.filter(name=name)
    b.delete()

    return redirect('manager_group')


#when the group action is clicked in the manager list users it will retrive this page which list groups and give option to add group
def users_group(request, pk):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})

    manager = Manager.objects.get(pk=pk)

    user = User.objects.get(username=manager.utxt)

    ugroup = []
    for i in user.groups.all():
        ugroup.append(i.name)
    '''
    if not ugroup:
        error = 'This user dont have group!'
        return render(request, 'back/error.html', {'error': error})
    '''
    group = Group.objects.all()

    return render(request, 'back/users_group.html', {'ugroup': ugroup, 'group':group, 'pk':pk})

def add_users_to_groups(request, pk):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    if request.method == 'POST':
        gname = request.POST.get('gname')
        
        group = Group.objects.get(name = gname)
        manager = Manager.objects.get(pk=pk)
        user = User.objects.get(username = manager.utxt)
        user.groups.add(group)
    
    return redirect('users_group', pk=pk)

def del_users_groups(request, pk, name):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1
    
    if perm == 0:
        error = "Access Denied"
        return render(request, 'back/error.html', {'error':error})
    
    group = Group.objects.get(name = name)
    manager = Manager.objects.get(pk=pk)
    user = User.objects.get(username = manager.utxt)
    user.groups.remove(group)
    
    return redirect('users_group', pk=pk)
