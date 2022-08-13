import random
from traceback import print_exception
from dateutil.relativedelta import relativedelta
from datetime import date, datetime
from django.shortcuts import render, redirect, HttpResponse
from display.models import *
from django.db.models import Q
from django.views.decorators.cache import cache_control


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def postads(request):
    if request.user.is_anonymous:
        return redirect('/')
    
    user = UserProfile.objects.filter(
        user=request.user).select_related().first()
    if (user.name == "Your Name" or user.address=="Your address" or user.phone=="0000000000" ):
        context={'warning':True}
        return render(request, 'postad.html',context)
    categories = Category.objects.all()
    context = {'category':categories}
    return render(request, 'postad.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def details(request, item):
    if request.user.is_anonymous:
        return redirect('/')
    
    elif request.method == 'GET' and item != 0:
        product = Product.objects.filter(id=item)
        wishlist = Wishlist.objects.filter(Q(user=request.user) & Q(product_id=item))
        flag="False"
        if(len(wishlist)!=0):
            flag="True"
       
        context = {'products':product,'wish':flag}
        return render(request, 'description.html', context)
    return render(request,'description.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def soldout(request, item=0):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'GET'):
        status = Status.objects.filter(id=2).first()
        prod = Product.objects.filter(Q(user=request.user) & Q(id=item)).first()
        prod.status = status
        prod.save()
    return redirect('/myorders/')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def getinformation(request, item=0):
    if request.user.is_anonymous:
        return redirect('/')
    
    if(request.method=='GET'):
        user_id = request.GET.get('user')
        user = UserProfile.objects.filter(user=user_id).first()
        uemail = User.objects.filter(id=user_id).first()
        lists = user.name + "+" + user.phone + "+" + user.address + "+" + uemail.email
        
        return HttpResponse(lists)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addtowishlist(request):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'GET'):
        product_id = request.GET.get('product_id')
        product = Product.objects.filter(id=product_id).first()
        wishlist_obj = Wishlist.objects.create(
            product=product, user=request.user)
        wishlist_obj.save()
        return HttpResponse('success')

    return redirect('/details/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showwishlist(request):
    if request.user.is_anonymous:
        return redirect('/')

    result = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {'wishlists': result}

    return render(request, 'wishlist.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def removewishlistpage(request, id):
    if request.user.is_anonymous:
        return redirect('/')

    Wishlist.objects.filter(Q(user=request.user) & Q(product_id=id)).delete()

    return redirect('/showwishlist/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    if request.user.is_anonymous:
        return redirect('/')
    user_profile = UserProfile.objects.filter(
        user=request.user).select_related()
    
    context = {"profiles": user_profile}
    return render(request, 'profile.html', context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def removewishlist(request):
    if request.user.is_anonymous:
        return redirect('/')
    if(request.method == 'GET'):
        book_id = request.GET.get('book_id')
        Wishlist.objects.filter(Q(user=request.user)
                                and Q(book_id=book_id)).delete()
        print('deleted successfully')

        return redirect('/book_search/0')
    redirect('/book_search/0')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def save_profile(request):
    if request.user.is_anonymous:
        return redirect('/')

    if(request.method == 'POST'):
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        mobile = request.POST.get('phone')
        print(mobile)
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.name = name
        user_profile.bio = bio
        user_profile.address = address
        user_profile.phone = mobile
        user_profile.save()
    print('profile saved successfully')
    return redirect('/profile/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def myorders(request):
    if request.user.is_anonymous:
        return redirect('/')
    result = Product.objects.filter(
        user=request.user).order_by('-pub_date')
    
    context = {'orderlist': result}
    return render(request, 'myorder.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def uploadads(request):
    if request.user.is_anonymous:
        return redirect('/')
    
    if(request.method == 'POST'):

        title = request.POST.get('title')
        user = request.user
        cat = request.POST.get('category')
        category = Category.objects.filter(id=cat).first()
        price = request.POST.get('price')
        descr=request.POST.get('desc')
        status = Status.objects.filter(id=1).first()
        pub_date= date.today()
        product_image=""
        if len(request.FILES)!=0:
            product_image = request.FILES['image']
        
        product = Product.objects.create(
            user=user,product_title=title, status=status, category=category, prod_desc=descr, price=price, pub_date=pub_date,product_image=product_image )
        product.save()
        
        context = {'sent': True}
        return render(request,'postad.html',context)
    return redirect('/postad/')
        