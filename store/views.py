from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder


def store(request):
    data = cartData(request)

    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartitems': cartitems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/checkout.html', context)


def product_detail(request, slug):
    data = cartData(request)

    cartitems = data['cartitems']

    product_detail = Product.objects.get(slug=slug)
    context = {'product_detail': product_detail, 'cartitems': cartitems}
    return render(request, 'store/product_detail.html', context)


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


def cat(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'store/index.html', context)


def track(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartitems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cartitems = order['get_cart_items']
    context = {'cartitem': cartitems}
    return render(request, 'store/track.html', context)


def updateitem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']
    print('Action:', action)
    print('Product:', productid)

    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderitem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderitem.quantity = (orderitem.quantity + 1)
    elif action == 'remove':
        orderitem.quantity = (orderitem.quantity - 1)
    elif action == 'delete':
        orderitem.delete()

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
    else:
        customer, order = guestOrder(request, data)

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

    return JsonResponse('Payment completed!', safe=False)
