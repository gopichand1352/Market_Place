from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,logout,login as auth_login
from django.views import View
from homepage.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.db.models.query import QuerySet
import razorpay
from razorpay.client import Client
import pkg_resources
from django.views.decorators.csrf import csrf_protect

# Create your views here.
def login(request):
    if request.method == 'POST':
        username=request.POST.get('email1')
        pass1=request.POST.get('password1')
        user=authenticate(username=username,password=pass1)
        if user is not None:
            auth_login(request,user)
            return redirect('http://127.0.0.1:8000/')
        else:
            messages.error(request,'Invalid Username or Password Credential.')
    return render(request,'homepage_design/login.html')

def logout_user(request):
    logout(request)
    return redirect('Login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('email1')
        email = request.POST.get('email1')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.error(request,'The User name already exists. Please choose another username.')
            elif User.objects.filter(email=email).exists():
                messages.error(request,'The Email already exists. Please choose another Email.')
            else:
                my_user=User.objects.create_user(username,email,pass1)
                messages.success(request,'User created successfully.')
                my_user.save()
                return redirect('Login')
        elif pass1!=pass2:
            messages.error(request,'Password and Confirm Password Missmatch.')
    return render(request,'homepage_design/register.html')


class ProductView(View):
    def get(self,request):
        prolen=Product.objects.all()
        plength=len(prolen)
        milkitems=Product.objects.filter(pcategory='MI')
        sweets=Product.objects.filter(pcategory='S')
        vegetables=Product.objects.filter(pcategory='V')
        fruits=Product.objects.filter(pcategory='F')
        soft_drink=Product.objects.filter(pcategory='SD')
        bake_item=Product.objects.filter(pcategory='BI')
        mlen=len(milkitems)
        slen=len(sweets)
        vlen=len(vegetables)
        f=len(fruits)
        sd=len(soft_drink)
        bitem=len(bake_item)
        return render(request,'homepage_design/base.html',{ 'products':prolen,'plength':plength,'mlen':mlen,'slen':slen,'vlen':vlen,'f':f,'sd':sd,'bitem':bitem,'milkitems':milkitems,'sweets':sweets,'vegetables':vegetables,'fruits':fruits,'soft_drink':soft_drink,'bake_item':bake_item})

@login_required(login_url='Login')
def sale(request):
    if request.method == 'POST':
        user=request.user
        pname=request.POST.get('nam')
        pcategory=request.POST.get('cat')
        pdescription=request.POST.get('dis')
        selling_price=request.POST.get('sp')
        discount_price=request.POST.get('dp')
        discount_percent=request.POST.get('dpp')
        image1=request.POST.get('im1')
        image2=request.POST.get('im2')
        image3=request.POST.get('im3')
        pro=Product(user=user,pname=pname,pcategory=pcategory,pdescription=pdescription,selling_price=selling_price,discount_price=discount_price,discount_percent=discount_percent,image1=image1,image2=image2,image3=image3)
        pro.save()
        return redirect('products')

    return render(request,'Sale/saleProduct.html')

@login_required(login_url='Login')
def cart(request,cpid):
    user=request.user
    product=Product.objects.get(id=cpid)
    Cart(user=user,product=product).save()
    return redirect('show_cart')

@login_required(login_url='Login')
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        length=len(cart)
        amount=0.0
        shipping_amount=70.0
        total_amount=0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for i in cart_product:
                temp_amount=(i.quantity * i.product.discount_price)
                amount+=temp_amount
                total_amount=amount+shipping_amount
            return render(request,'cart/cart1.html',{'cart':cart,'length':length,'amount':amount,'total_amount':total_amount,'shipping_amount':shipping_amount})
        else:
            return render(request,'cart/no_product_cart.html')
    return render(request,'cart/no_product_cart.html')
    
    
def plus(request,cid):
    product=Cart.objects.get(id=cid)
    product.quantity+=1
    product.save()
    return redirect('show_cart')

def minus(request,cid):
    product=Cart.objects.get(id=cid)
    if product.quantity>1:
        product.quantity=product.quantity-1
        product.save()
    else:
        product.delete()
    return redirect('show_cart')

def wishlist(request):
    return render(request,'wishlist/wishlist.html')



@login_required(login_url='Login')
def myorders(request):
    if request.method == 'POST':
       request=request.POST
       print(request)
    user=request.user
    orders=OrderPlaced.objects.filter(user=user)
    return render(request,'myorders/myorders.html',{'orders':orders})


def payment_done(request):
    if request.method=='POST':
        user=request.user
        add=Customer.objects.filter(user=user)
        products=Cart.objects.filter(user=user)
        custid=request.POST.get('custid')
        customer=Customer.objects.get(id=custid)
        cart=Cart.objects.filter(user=user)
         
         #create razorpay client
        client=Client(auth=('rzp_test_RP2M8nHYEP9X7b','sJFjqZvN6mymDPDUUgoyMEfK'))

        amount=0.0
        shipping_amount=70.0
        total_amount=0
        for c in cart:
            temp_amount=(c.quantity * c.product.discount_price)

            amount+=temp_amount
            total_amount=amount+shipping_amount
            
            #create order
            response_payment=client.order.create(dict(amount=total_amount * 100,currency='INR'))
            
            #order id
            order_id=response_payment['id']
            order_status=response_payment['status']

            if order_status == 'created':
                OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,price=total_amount,order_id=order_id).save()
                response_payment['name']=customer.customer_name
                c.delete()
                return render(request,'cart/check_out.html',{'payment':response_payment,'amount':amount,'shipping_amount':shipping_amount,'total_amount':total_amount})
        return redirect('myorders')

@login_required(login_url='Login')
def profile(request):
    if request.method=='POST':
        user=request.user
        name=request.POST.get('name')
        phoneNumber=request.POST.get('phone')
        locality=request.POST.get('locality')
        city=request.POST.get('city')
        zipcode=request.POST.get('zipcode')
        country=request.POST.get('country')
        state=request.POST.get('state')
        reg=Customer(user=user,customer_name=name,phoneNumber=phoneNumber,customer_locality=locality,customer_city=city,customer_zipcode=zipcode,customer_country=country,customer_state=state)
        reg.save()
        messages.success(request,'Profile Updated Successfully..')
    
    return render(request,'profile/profile.html')


@login_required(login_url='Login')
def myself(request):
    addr=Customer.objects.filter(user=request.user)
    leng=len(addr)
    print(leng)
    return render(request,'profile/address.html',{'addr':addr})


def products(request):
    return render(request,'product_templates/base.html')

def milk_items_page(request):
    prolen1=Product.objects.all()
    plength1=len(prolen1)
    milkitems1=Product.objects.filter(pcategory='MI')
    mlen1=len(milkitems1)
    return render(request,'product_templates/milk_products.html',{'plength1':plength1,'mlen1':mlen1,'milkitems1':milkitems1})

def soft_drink_page(request):
    prolen2=Product.objects.all()
    plength2=len(prolen2)
    drinks=Product.objects.filter(pcategory='SD')
    dlen=len(drinks)
    return render(request,'product_templates/soft_drinks.html',{'plength2':plength2,'dlen':dlen,'drinks':drinks})

def sweets(request):
    prolen3=Product.objects.all()
    plength3=len(prolen3)
    sweets3=Product.objects.filter(pcategory='S')
    slen3=len(sweets3)
    return render(request,'product_templates/sweets.html',{'plength3':plength3,'slen3':slen3,'sweets3':sweets3})

def fruits(request):
    prolen4=Product.objects.all()
    plength4=len(prolen4)
    fruits=Product.objects.filter(pcategory='F')
    flen=len(fruits)
    return render(request,'product_templates/fruits.html',{'plength4':plength4,'flen':flen,'fruits':fruits})

def vegetables(request):
    prolen5=Product.objects.all()
    plength5=len(prolen5)
    vegetables=Product.objects.filter(pcategory='V')
    vlen=len(vegetables)
    return render(request,'product_templates/vegetables.html',{'plength5':plength5,'vlen':vlen,'vegetables':vegetables})

def bake_items(request):
    prolen6=Product.objects.all()
    plength6=len(prolen6)
    bake_items=Product.objects.filter(pcategory='BI')
    blen=len(bake_items)
    return render(request,'product_templates/bake_items.html',{'plength6':plength6,'blen':blen,'bake_items':bake_items})


class product_detail(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        return render(request,'product_templates/product_detail.html',{'product':product})
    

def cart_remove(request,pid):
    Cart.objects.filter(product=pid).delete()
    return redirect('show_cart')

def check_out(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    if len(add)>0:
        products=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        total_amount=0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
           for i in cart_product:
               temp_amount=(i.quantity * i.product.discount_price)
               amount+=temp_amount
               total_amount=amount+shipping_amount
        return render(request,'cart/check_out.html',{'add':add,'amount':amount,'shipping_amount':shipping_amount,'total_amount':total_amount,'products':products})
    else:
        return render(request,'profile/profile.html')
      
def cancle_order(request,oid):
    x=int(oid)
    product=OrderPlaced.objects.get(id=x)
    product.delete()
    return redirect('myorders')

def delete_address(request,addid):
    address=Customer.objects.get(id=addid)
    address.delete()
    return redirect('myself')
    

