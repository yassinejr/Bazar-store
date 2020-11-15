from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *


# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartitem = order['get_cart_items']

    products = Product.objects.all()
    context = {'items':items,'products': products, 'cartitem': cartitem}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartitem = order['get_cart_items']
    context = {'items': items, 'order': order, 'cartitem': cartitem}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartitem = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartitem': cartitem}
    return render(request, 'store/checkout.html', context)


def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/product.html', context)


def login(request):
    context = {}
    return render(request, 'store/login.html', context)


def password_reset(request):
    context = {}
    return render(request, 'store/password_reset.html', context)


def sign(request):
    context = {}
    return render(request, 'store/signup.html', context)


def profile(request):
    context = {}
    return render(request, 'store/profile.html', context)


def edit_profile(request):
    context = {}
    return render(request, 'store/edit_profile.html', context)


def success(request):
    context = {}
    return render(request, 'store/order_success.html', context)


def track(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitem = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitem = order['get_cart_items']
    context = {'cartitem': cartitem}
    return render(request, 'store/track.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']

    print('productid:', productid)
    print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = orderitem.quantity + 1
    elif action == 'remove':
        orderitem.quantity = orderitem.quantity - 1
    orderitem.save()

    if orderitem.quantity <= 0:
        orderitem.delete()
    return JsonResponse('Item was added', safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                country=data['shipping']['country'],
            )
    else:
        print('user is not logged in')
    return JsonResponse('Payment completed!', safe=False)
