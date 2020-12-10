from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('shopping-cart/', views.shopping_cart, name="shopping-cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('<slug:slug>', views.product_detail, name="product_detail"),
    path('track/', views.track, name="track"),
    path('update_item/', views.updateitem, name="updateitem"),
    path('process_order/', views.processorder, name="processorder"),
]

