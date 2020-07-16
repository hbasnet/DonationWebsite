from django.shortcuts import render, get_object_or_404, redirect
from .models import Cat

# Create your views here.
def cat_list(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    cat = Cat.objects.all()
    return render(request, 'back/cat_list.html', {'cat':cat})

def cat_add(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name == '':
            error = "All fields required"
            return render(request, 'back/error.html', {'error':error})
        
        if len(Cat.objects.filter(name=name)) != 0:
            error = "This category already exists"
            return render(request, 'back/error.html', {'error':error})
        
        b = Cat(name = name)
        b.save()
        return redirect('cat_list')

    return render(request, 'back/cat_add.html')
