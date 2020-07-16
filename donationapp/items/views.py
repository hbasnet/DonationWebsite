from django.shortcuts import render, get_object_or_404, redirect
from .models import Items
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat

#for pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def items_detail(request, word):
    
    site = Main.objects.get(pk=1) #for this we don't have to use for loops
    items = Items.objects.all().order_by('-pk') #latest items at first
    cat = Cat.objects.all() #to show categories in footer
    subcat = SubCat.objects.all()
    lastitems = Items.objects.all().order_by('-pk')[:3] #latest 3 items at first

    showitems = Items.objects.filter(name=word)
    
    #to list the items according to views
    popitems = Items.objects.all().order_by('-show')[:3]
    
    #to print number of views
    try:
        myitems = Items.objects.get(name=word)
        myitems.show = myitems.show + 1
        myitems.save()
    except:
        print("Can't Add Show")

    return render(request, 'front/items_detail.html', {'site':site, 'items':items, 'cat':cat, 'subcat':subcat, 'lastitems':lastitems, 'showitems':showitems, 'popitems':popitems})


def items_list(request):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    itemss = Items.objects.all()
    
    #pagination
    paginator = Paginator(itemss,2)
    page = request.GET.get('page')
    
    try:
        items = paginator.page(page)
    
    except EmptyPage:
        items = paginator.page(paginator.num_page)
    
    except PageNotAnInteger:
        items = paginator.page(1)
    
    return render(request, 'back/items_list.html', {'items': items})


def items_add(request):

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

    # to make a choose sub category option we need to get all the sub category
    cat = SubCat.objects.all()

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
            return render(request, 'back/error.html', {'error': error})

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
                    ###############
                    return redirect('items_list')

                else:
                    fs = FileSystemStorage()  # if file is not supported then delete the image from media
                    fs.delete(filename)

                    error = "This file is not less that 5MB"
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs = FileSystemStorage()  # if file is not supported then delete the image from media
                fs.delete(filename)

                error = "This file is not supported"
                return render(request, 'back/error.html', {'error': error})

        except:
            fs = FileSystemStorage()  # if file is not supported then delete the image from media
            fs.delete(filename)
            error = "please input your image"
            return render(request, 'back/error.html', {'error': error})

    return render(request, 'back/items_add.html', {'cat': cat})

# creating a function for new delete


def items_delete(request, pk):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    try:
        # b = Items.objects.filter(pk=pk) #filter is used because it won't give error if nth is present
        b = Items.objects.get(pk=pk)
        fs = FileSystemStorage()  # these two lines delete image from media
        fs.delete(b.picname)
        
        ocatid = Items.objects.get(pk=pk).ocatid
        
        b.delete()
        
        count = len(Items.objects.filter(ocatid=ocatid))
        
        m = Cat.objects.get(pk=ocatid)
        m.count = count
        m.save()
        
    except:
        error = "Something is wrong"
        return render(request, 'back/error.html', {'error': error})
    return redirect('items_list')


def items_edit(request, pk):
    
    #login check start
    if not request.user.is_authenticated:
        return redirect('mylogin')
    #login check end
    
    if len(Items.objects.filter(pk=pk)) == 0:
        error = "Something is wrong"
        return render(request, 'back/error.html', {'error': error})

    items = Items.objects.get(pk=pk)
    cat = SubCat.objects.all()

    if request.method == 'POST':
        itemstitle = request.POST.get('itemstitle')
        itemscat = request.POST.get('itemscat')
        itemstxtshort = request.POST.get('itemstxtshort')
        itemstxt = request.POST.get('itemstxt')
        #owner = request.POST.get('owner')
        itemsid = request.POST.get('itemscat')

        # validation for the form
        if itemstitle == "" or itemstxtshort == "" or itemstxt == "" or itemscat == "":
            error = 'All Fields Required!'
            return render(request, 'back/error.html', {'error': error})

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

                    # this time we are not saving the field value in data base directly
                    b = Items.objects.get(pk=pk)

                    # old image needs to be deleted

                    fss = FileSystemStorage()  # if file is not supported then delete the image from media
                    fss.delete(b.picname)

                    b.name = itemstitle
                    b.short_txt = itemstxtshort
                    b.body_txt = itemstxt
                    b.picname = filename
                    b.picurl = url
                    b.catname = itemsname
                    b.catid = itemsid

                    b.save()
                    return redirect('items_list')

                else:
                    fs = FileSystemStorage()  # if file is not supported then delete the image from media
                    fs.delete(filename)

                    error = "This file is not less that 5MB"
                    return render(request, 'back/error.html', {'error': error})
            else:
                fs = FileSystemStorage()  # if file is not supported then delete the image from media
                fs.delete(filename)

                error = "This file is not supported"
                return render(request, 'back/error.html', {'error': error})

        except:
            #eventhough image is not chosen it saves the data doesn't give error
            itemsname = SubCat.objects.get(pk=itemsid).name

            b = Items.objects.get(pk=pk)

            fss = FileSystemStorage()
            fss.delete(b.picname)

            b.name = itemstitle
            b.short_txt = itemstxtshort
            b.body_txt = itemstxt
            b.catname = itemsname
            b.catid = itemsid

            b.save()
            return redirect('items_list')

    return render(request, 'back/items_edit.html', {'pk': pk, 'items': items, 'cat': cat})
