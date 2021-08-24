from django.shortcuts import render,redirect
from .models import Customer,Product,Order,OrderItem,ShippingAddress,Contact
from django.http import JsonResponse
import json
from django.db.models import Q
import datetime
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import SignupForm,ContactForm
# Create your views here.
def store(request):
    product=Product.objects.all()
    smartphones=Product.objects.filter(category__contains='smartphones')
    tablets=Product.objects.filter(category__contains='tablets')
    television=Product.objects.filter(category__contains='television')
    smartwatches=Product.objects.filter(category__contains='smartwatches')
  
    
    
    context={
        'product':product,
        'smartphones':smartphones,
        'tablets':tablets,
        'television':television,
        'smartwatches':smartwatches,
        
        
    }
    return render(request,"ecommerce/store.html",context)
def product(request,id):
    product=Product.objects.get(id=id)
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
        items=order.order.all()
        cartItems=order.get_total_item
        
    else:
        items=[]
        #if user is not logged in
        order={
            'get_total':0,'get_total_item':0
        }
        cartItems=order['get_total_item']
    
    context={"product":product
             ,
             'items':items,
        'order':order,
        'cartItems':cartItems}
    
    return render(request,'ecommerce/product.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
        items=order.order.all()
        cartItems=order.get_total_item
        
    else:
        items=[]
        #if user is not logged in
        order={
            'get_total':0,'get_total_item':0
        }
        cartItems=order['get_total_item']
    
    context={
        'items':items,
        'order':order,
        'cartItems':cartItems
        
    }
    return render(request,"ecommerce/cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        
        items=order.order.all()
        cartItems=order.get_total_item
    else:
        items=[]
        #if user is not logged in
        order={
            'get_total':0,'get_total_item':0
        }
        
        cartItems=order['get_total_item']
    
    context={
        'items':items,
        'order':order,
        'cartItems':cartItems
        
    }
    return render(request,"ecommerce/checkout.html",context)



def updateItem(request):
    data=json.loads(request.body)
    productId=data['productID']
    action=data['action']
    print("ID",productId)
    print("ACTION:",action)
    
    customer=Customer.objects.get(user=request.user)
    product=Product.objects.get(id=productId)
    
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    
    orderItem,creat=OrderItem.objects.get_or_create(order=order,product=product)
    
    if action == 'add':
        orderItem.quantity+=1
    elif action== 'remove':
        orderItem.quantity-=1
    orderItem.save()
    
    if orderItem.quantity <=0:
        orderItem.delete()
    
    return JsonResponse("Item was added",safe=False)
def processOrder(request):
    print("DATA:",request.body)
    transaction_id=datetime.datetime.now().timestamp()
    
    data=json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=Customer.objects.get(user=request.user)
        
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        total=float(data['userDetail']['total'])
        
        order.transaction_id=transaction_id
        print(order.transaction_id)
        if total == order.get_total:
            order.complete=True
        order.save()
        ShippingAddress.objects.create(
            customer=customer,order=order,
            address=data['shippingDetails']['address'],
            city=data['shippingDetails']['city'],
            country=data['shippingDetails']['country'],
            zipcode=data['shippingDetails']['zip']
        )
    else:
        print("USer not logged in")
    
    
    return JsonResponse("Payment done",safe=False)
def search(request):
    
    if request.method == 'POST':
        search=request.POST.get('search')
        
        product=Product.objects.filter(Q(name__startswith=search))
        
    context={
        'search':search,
        'product':product,      
        
    }
      
        
    return render(request,'ecommerce/search.html',context)

def login_view(request):
    if request.method == 'POST':
        name=request.POST['name']
        print(name)
        password=request.POST['password']
        
        user=authenticate(User,username=name,password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect("store")
        else:
            return render(request,'ecommerce/login.html')
    else:
        
        return render(request,'ecommerce/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            
            user=authenticate(username=username,password=raw_password)
            login(request,user)
            return redirect('login')
        else:
            pass
    else:
        form=SignupForm()
        return render(request,'ecommerce/register.html',{'form':form})
def contact(request):
    if request.method == 'POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form=ContactForm()
    
    
    return render(request,"ecommerce/contact.html",{'form':form})


#i will add 1)slideshow,= 2)register 3)payment 4)ajax