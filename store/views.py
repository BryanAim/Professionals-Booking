import email
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from professional_service.models import Client
from store.models import Product, Cart, ServiceOrder
from .utils import searchProducts
from django.views.decorators.csrf import csrf_exempt


# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver


# Create your views here.

# function to return views for the urls

@csrf_exempt
@login_required(login_url="login")
def store_single_product(request,pk):
     if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        products = Product.objects.get(serial_number=pk)
        orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'client': client, 'products': products,'carts': carts,'order': order, 'orders': orders}
            return render(request, 'store/product-single.html',context)
        else:
            context = {'client': client, 'products': products,'carts': carts,'orders': orders}
            return render(request, 'store/product-single.html',context)
     else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')  

@csrf_exempt
@login_required(login_url="login")
def store_shop(request):
    if request.user.is_authenticated and request.user.is_client:
        
        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
        carts = Cart.objects.filter(user=request.user, purchased=False)
        
        products, search_query = searchProducts(request)
        
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'client': client, 'products': products,'carts': carts,'order': order, 'orders': orders, 'search_query': search_query}
            return render(request, 'Store/shop.html', context)
        else:
            context = {'client': client, 'products': products,'carts': carts,'orders': orders, 'search_query': search_query}
            return render(request, 'Store/shop.html', context)
    
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')  

@csrf_exempt
@login_required(login_url="login")
def checkout(request):
    return render(request, 'store/checkout.html')

@csrf_exempt
@login_required(login_url="login")
def add_to_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        
        item = get_object_or_404(Product, pk=pk)
        order_item = Cart.objects.get_or_create(item=item, user=request.user, purchased=False)
        order_qs = ServiceOrder.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item[0].quantity += 1
                order_item[0].save()
                # messages.warning(request, "This item quantity was updated!")
                context = {'client': client,'products': products, 'order': order}
                return render(request, 'store/shop.html', context)
            
            else:
                order.orderitems.add(order_item[0])
                # messages.warning(request, "This item is added to your cart!")
                context = {'client': client,'products': products,'order': order}
                return render(request, 'store/shop.html', context)
        else:
            order = ServiceOrder(user=request.user)
            order.save()
            order.orderitems.add(order_item[0])
            # messages.warning(request, "This item is added to your cart!")
            context = {'client': client,'products': products,'order': order}
            return render(request, 'store/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html')  

@csrf_exempt
@login_required(login_url="login")
def cart_view(request):
    if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        
        carts = Cart.objects.filter(user=request.user, purchased=False)
        orders = ServiceOrder.objects.filter(user=request.user, ordered=False)
        if carts.exists() and orders.exists():
            order = orders[0]
            context = {'carts': carts,'order': order}
            return render(request, 'Store/cart.html', context)
        else:
            messages.warning(request, "You don't have any item in your cart!")
            context = {'client': client,'products': products}
            return render(request, 'store/shop.html', context)
    else:
        logout(request)
        messages.info(request, 'Not Authorized')
        return render(request, 'client-login.html') 

@csrf_exempt
@login_required(login_url="login")
def remove_from_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        
        item = get_object_or_404(Product, pk=pk)
        order_qs = ServiceOrder.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                order.orderitems.remove(order_item)
                order_item.delete()
                messages.warning(request, "This item was remove from your cart!")
                context = {'carts': carts,'order': order}
                return render(request, 'Store/cart.html', context)
            else:
                messages.info(request, "This item was not in your cart")
                context = {'client': client,'products': products}
                return render(request, 'store/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'client': client,'products': products}
            return render(request, 'store/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html') 


@csrf_exempt
@login_required(login_url="login")
def increase_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Product, pk=pk)
        order_qs = ServiceOrder.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity >= 1:
                    order_item.quantity += 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Store/cart.html', context)
            else:
                messages.warning(request, f"{item.name} is not in your cart")
                context = {'client': client,'products': products}
                return render(request, 'store/shop.html', context)
        else:
            messages.warning(request, "You don't have an active order")
            context = {'client': client,'products': products}
            return render(request, 'store/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html') 


@csrf_exempt
@login_required(login_url="login")
def decrease_cart(request, pk):
    if request.user.is_authenticated and request.user.is_client:
         
        client = Client.objects.get(user=request.user)
        products = Product.objects.all()
        carts = Cart.objects.filter(user=request.user, purchased=False)
        item = get_object_or_404(Product, pk=pk)
        order_qs = ServiceOrder.objects.filter(user=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item=item).exists():
                order_item = Cart.objects.filter(item=item, user=request.user, purchased=False)[0]
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    order_item.save()
                    messages.warning(request, f"{item.name} quantity has been updated")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Store/cart.html', context)
                else:
                    order.orderitems.remove(order_item)
                    order_item.delete()
                    messages.warning(request, f"{item.name} item has been removed from your cart")
                    context = {'carts': carts,'order': order}
                    return render(request, 'Store/cart.html', context)
            else:
                messages.info(request, f"{item.name} is not in your cart")
                context = {'client': client,'products': products}
                return render(request, 'store/shop.html', context)
        else:
            messages.info(request, "You don't have an active order")
            context = {'client': client,'products': products}
            return render(request, 'store/shop.html', context)
    else:
        logout(request)
        messages.error(request, 'Not Authorized')
        return render(request, 'client-login.html') 
# Create your views here.
