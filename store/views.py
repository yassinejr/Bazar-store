from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from accounts.models import Profile


def store(request):
    data = cartData(request)

    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'products': products, 'categories': categories, 'cartitems': cartitems, 'items': items, 'order': order}
    return render(request, 'store/product.html', context)


def shopping_cart(request):
    data = cartData(request)

    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/shopping_cart.html', context)


def quick_cart(request):
    data = cartData(request)

    cartitems = data['cartitems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartitems': cartitems}
    return render(request, 'store/index.html', context)


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
    order = data['order']
    items = data['items']

    product_detail = Product.objects.get(slug=slug)
    context = {'product_detail': product_detail, 'cartitems': cartitems, 'items': items, 'order': order}
    return render(request, 'store/product-detail2.html', context)


def blog(request):
    # blogs = Blog.objects.all()

    # context = {'blog':blogs}
    return render(request, 'store/blog.html')

def blog_detail(request):
    # blogs = Blog.objects.all()
    # context = {'blog':blogs}
    return render(request, 'store/blog-detail.html')

def contact(request):
    # blogs = Blog.objects.all()
    # context = {'blog':blogs}
    return render(request, 'store/contact.html')

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
