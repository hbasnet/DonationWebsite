from django.shortcuts import render, get_object_or_404, redirect
from .models import Main
from items.models import Items
from cat.models import Cat
from subcat.models import SubCat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from manager.models import Manager

import datetime

#for pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from ipware import get_client_ip

# Create your views here.

def home(request):
    
    #sitename = "Mysite | Home" #this is the variable can be sent to html
    #site = Main.objects.filter(pk=1) #or we can send database data for this we have to use for loops {% for i in sitename %} {% endfor %}
    #there is also other way to get data from database
    site = Main.objects.get(pk=1) #for this we don't have to use for loops
    items = Items.objects.all().order_by('-pk') #latest items at first
    cat = Cat.objects.all() #to show categories in footer
    
    subcat = SubCat.objects.all()
    
    lastitems = Items.objects.all().order_by('-pk')[:3] #latest 3 items at first
    
    #to list the items according to views
    popitems = Items.objects.all().order_by('-show')[:3]
    
    return render(request, 'front/home.html', {'site':site, 'items':items, 'cat':cat, 'subcat':subcat, 'lastitems':lastitems, 'popitems':popitems})

def about(request):
    
    site = Main.objects.get(pk=1)
    
    #copied from home to have same menu bar in about page as home page
    #because it first load the master page so we have already done for home page with same queries
    items = Items.objects.all().order_by('-pk') #latest items at first
    cat = Cat.objects.all() #to show categories in footer
    
    subcat = SubCat.objects.all()
    
    lastitems = Items.objects.all().order_by('-pk')[:3] #latest 3 items at first
    
    #to list the items according to views
    popitems = Items.objects.all().order_by('-show')[:3]
    
    
    return render(request, 'front/about.html', {'site':site, 'items':items, 'cat':cat, 'subcat':subcat, 'lastitems':lastitems, 'popitems':popitems})

def panel(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    '''
    ip, is_routable = get_client_ip(request)
    
    if ip is None:
        ip = "0.0.0"
    else:
        if is_routable:
            ipv = "public"
        else:
            ipv = "private"
    
    print(ip, ipv)
    '''
    return render(request, 'back/home.html')


def mylogin(request):
    
    if request.method == 'POST':
        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')
        
        if utxt != "" and ptxt != "":
            user = authenticate(username = utxt, password = ptxt)
            
            #if there is no user of the following name and pass will give None
            if user != None:
                login(request, user)
                return redirect('home')
    
    return render(request, 'front/login.html')

def myregister(request):
    
    if request.method == 'POST':
        
        name = request.POST.get('name')
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            msg = "Your passwords didn't match"
            return render(request, 'front/msgbox.html', {'msg':msg})
        
        if len(password1) < 8:
                msg = 'Password must have length > 8!'
                return render(request, 'front/msgbox.html', {'msg':msg})
            
        count1 = 0
        count2 = 0
        count3 = 0
        count4 = 0
        for i in password1:
            if i >= "0" and i <= "9":
                count1 = 1
            if i >= "A" and i <= "Z":
                count2 = 1
            if i >= "a" and i <= "z":
                count3 = 1
            if i >= "!" and i <= "(":
                count4 = 1
            
        if count1 == 0 or count2 == 0 or count3 == 0 or count4 == 0:
            msg = 'Password must be strong'
            return render(request, 'front/msgbox.html', {'msg':msg})
            
        #check if the username and email exists before
        if len(User.objects.filter(username = uname)) == 0 and len(User.objects.filter(email = email)) == 0:
            user = User.objects.create_user(username = uname, email=email, password=password1)
            b = Manager(name = name, utxt = uname, email=email)
            b.save()

    return render(request, 'front/login.html')

def mylogout(request):
    
    logout(request)
    
    return redirect('mylogin')

def site_setting(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    if request.method == 'POST':
        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')
        
        if fb == "" : fb = "#"
        if tw == "" : tw = "#"
        if yt == "" : yt = "#"
        if link == "" : link = "#"
        
        if name=="" or tell == "" or txt == "":
            error = 'All Fields Required!'
            return render(request, 'back/error.html', {'error': error})
        
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)
            
            picurl = url
            picname = filename
            
        except:
            
            picurl = "-"
            picname = "-"
        
        try:
            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)
            
            picurl2 = url2
            picname2 = filename2
            
        except:
            
            picurl2 = "-"
            picname2 = "-"
            
        b = Main.objects.get(pk=1)
        b.name = name
        b.tell = tell
        b.fb = fb
        b.tw = tw
        b.yt = yt
        b.link = link
        b.about = txt
        if picurl != "-": b.picurl = picurl
        if picname != "-": b.picname = picname
        if picurl2 != "-": b.picurl2 = picurl2
        if picname2 != "-": b.picname2 = picname2
        b.save()
            
    
    site = Main.objects.get(pk=1)
    
    return render(request, 'back/setting.html', {'site':site})

def about_setting(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    if request.method == 'POST':
        txt = request.POST.get('txt')
        
        if txt == "":
            error = 'All Fields Required!'
            return render(request, 'back/error.html', {'error': error})
        
        b = Main.objects.get(pk=1)
        b.abouttxt = txt
        b.save()
    
    about = Main.objects.get(pk=1).abouttxt
    
    return render(request, 'back/about_setting.html', {'about':about})

def contact(request):
    
    site = Main.objects.get(pk=1) #for this we don't have to use for loops
    items = Items.objects.all().order_by('-pk') #latest items at first
    cat = Cat.objects.all() #to show categories in footer
    
    subcat = SubCat.objects.all()
    
    lastitems = Items.objects.all().order_by('-pk')[:3] #latest 3 items at first
    
    #to list the items according to views
    popitems = Items.objects.all().order_by('-show')[:3]
    
    return render(request, 'front/contact.html', {'site':site, 'items':items, 'cat':cat, 'subcat':subcat, 'lastitems':lastitems, 'popitems':popitems})

def change_pass(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    if request.method == 'POST':
        
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
                                
        if oldpass == "" or newpass == "":
            error = 'All Fields Required!'
            return render(request, 'back/error.html', {'error': error})
        
        user = authenticate(username = request.user, password = oldpass)
        
        if user != None:
            
            if len(newpass) < 8:
                error = 'Password must have length > 8!'
                return render(request, 'back/error.html', {'error': error})
            
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            for i in newpass:
                if i >= "0" and i <= "9":
                    count1 = 1
                if i >= "A" and i <= "Z":
                    count2 = 1
                if i >= "a" and i <= "z":
                    count3 = 1
                if i >= "!" and i <= "(":
                    count4 = 1
            
            if count1 == 1 and count2 == 1 and count3 == 1 and count4 == 1:
                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')
            
            else:
                error = 'Password is not strong!'
                return render(request, 'back/error.html', {'error': error})
                
        else:
            error = 'Password is not correct!'
            return render(request, 'back/error.html', {'error': error})
    
    return render(request, 'back/changepass.html')

def post_items(request):
    
       #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1:
        day = "0" + str(day)
    if len(str(month)) == 1:
        month = "0" + str(month)

    today = str(year) + "/" + str(month) + "/" + str(day)
    time = str(now.hour) + ":" + str(now.minute)
    
    site = Main.objects.get(pk=1)
    
    #copied from home to have same menu bar in about page as home page
    #because it first load the master page so we have already done for home page with same queries
    items = Items.objects.all().order_by('-pk') #latest items at first
    cat = Cat.objects.all() #to show categories in footer
    popitems = Items.objects.all().order_by('-show')[:3]
    subcat = SubCat.objects.all()

    # if the request is post we save the data into following variables
    if request.method == 'POST':
        itemstitle = request.POST.get('itemstitle')
        #itemscat = request.POST.get('itemscat')
        itemstxtshort = request.POST.get('itemstxtshort')
        itemstxt = request.POST.get('itemstxt')
        #owner = request.POST.get('owner')
        itemsid = request.POST.get('itemscat')

        # validation for the form
        if itemstitle == "" or itemstxtshort == "" or itemstxt == "":# or itemscat == "":
            error = 'All Fields Required!'
            return render(request, 'front/front_error.html', {'error': error})

        # to remove the error created by not choosing any file
        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            # if the image has same name generate the random name
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)  # url to download from page

            if str(myfile.content_type).startswith("image"):
                if myfile.size < 5000000:
                    itemsname = SubCat.objects.get(pk=itemsid).name
                    ocatid = SubCat.objects.get(pk=itemsid).catid #this to keep count of main category not sub category
                    
                    b = Items(name=itemstitle, short_txt=itemstxtshort, body_txt=itemstxt, date=today, time=time,
                             picname=filename, picurl=url, owner=request.user, catname=itemsname, catid=itemsid, show=0, ocatid=ocatid)
                    b.save()
                     #########
                     #I don't know how this is working
                    count = len(Items.objects.filter(ocatid=ocatid))
                    
                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()
                    ###############must redirect to user profile where we can see list of items posted
                    return redirect('/')

                else:
                    fs = FileSystemStorage()  # if file is not supported then delete the image from media
                    fs.delete(filename)

                    error = "This file is not less that 5MB"
                    return render(request, 'front/front_error.html', {'error': error})
            else:
                fs = FileSystemStorage()  # if file is not supported then delete the image from media
                fs.delete(filename)

                error = "This file is not supported"
                return render(request, 'front/front_error.html', {'error': error})

        except:
            fs = FileSystemStorage()  # if file is not supported then delete the image from media
            fs.delete(filename)
            error = "please input your image"
            return render(request, 'front/front_error.html', {'error': error})
    
    return render(request, 'front/post_items.html', {'site':site, 'items':items, 'cat':cat, 'subcat':subcat, 'popitems':popitems})