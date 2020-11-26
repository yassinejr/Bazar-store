from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.db.models.signals import post_save


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return str(self.name)


def create_customer(sender, **kwargs):
    if kwargs['created']:
        print(kwargs)
        user = User.objects.get(username=kwargs['instance'])
        user_name = user.first_name + " " + user.last_name
        print (user_name)
        user_customer = Customer.objects.create(
            user=kwargs['instance'],
            name=user_name,
            email=user.email,
        )


post_save.connect(create_customer, sender=User)


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, verbose_name=_('Product name'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name=_('Category'))
    brand = models.ForeignKey('settings.Brand', on_delete=models.CASCADE, null=True, blank=True,
                              verbose_name=_('Brand'))
    description = models.TextField(max_length=500, null=True, default='', verbose_name=_('Description'))
    price = models.FloatField(verbose_name=_('Price'))
    coast = models.FloatField(default=0, verbose_name=_('Coast'))
    discount = models.FloatField(null=True, blank=True, verbose_name=_('Discount'))
    digital = models.BooleanField(default=False, null=True, blank=True, verbose_name=_('Digital'))
    image = models.ImageField(upload_to='images/product/', null=True, blank=True, verbose_name=_('Image'))
    created_at = models.DateTimeField(default=datetime.now, null=True, blank=True, verbose_name=_('Created at'))
    slug = models.SlugField(blank=True, null=True, verbose_name=_('Slug'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name=_('Category name'))
    category_parent = models.ForeignKey('self', limit_choices_to={'category_parent__isnull': True},
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True)
    main_cat_desc = models.TextField(max_length=500, verbose_name=_('Description'))
    main_cat_img = models.ImageField(upload_to='images/category/', null=True, blank=True,
                                     verbose_name=_('Category image'))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.category_name)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Customer'))
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    complete = models.BooleanField(default=False, null=True, blank=True, verbose_name=_('Complete'))
    transaction_id = models.CharField(max_length=200, null=True, verbose_name=_('Transaction id'))

    def __str__(self):
        return str(self.transaction_id)

    @property
    def shipping(self):
        shipping = False
        orderitem = self.orderitem_set.all()
        for i in orderitem:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product'))
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Order'))
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name=_('Quantity'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('Date added'))

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Customer'))
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Order'))
    address = models.CharField(max_length=200, null=True, verbose_name=_('Adress'))
    city = models.CharField(max_length=200, null=True, verbose_name=_('City'))
    state = models.CharField(max_length=200, null=True, verbose_name=_('State'))
    zipcode = models.CharField(max_length=200, null=True, verbose_name=_('Zipcode'))
    country = models.CharField(max_length=200, null=True, verbose_name=_('Country'))
    date_added = models.DateTimeField(auto_now_add=True, verbose_name=_('Date added'))

    def __str__(self):
        return str(self.address)
