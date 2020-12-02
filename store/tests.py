import os
import pathlib
import unittest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.db.models import Max
from selenium.webdriver.firefox.webdriver import WebDriver
from django.test import TestCase, Client
from .models import Product, Category
from bazar import settings

from selenium import webdriver


# Finds the Uniform Resource Identifier of a file
def file_uri(filename):
    return pathlib.Path(os.path.abspath(filename)).as_uri()


# Sets up web driver using Google chrome
driver = webdriver.Chrome()


class ProductTestCase(TestCase):
    """
    Contains helper methods, used on many places
    by other classes.
    """

    def setUp(self):
        # create user
        user_info = {
            'first_name': 'Tester',
            'last_name': 'Testing',
            'username': 'tester',
            'password': 'topsecret2020',
        }
        self.user = User.objects.create(**user_info)

        # create category
        """
        Creates a testing category and a product in this category.
        Uploads a test product image.
        """
        test_image_src = settings.MEDIA_ROOT + os.sep + "/images/test/test-img.png"
        if not os.path.isfile(test_image_src):
            raise unittest.SkipTest("Test image for upload missing!")
        category = Category.objects.create(category_name="test-cat")
        test_image_upload = SimpleUploadedFile(
            name=test_image_src,
            content=open(test_image_src, 'rb').read(),
            content_type='image/png'
        )
        # create products
        p1 = {'name': 'product1',
              'category': category,
              'description': 'test',
              'price': 120,
              'coast': 80,
              'discount': 0,
              'digital': True,
              'image': test_image_upload,
              'slug': 'product1'}
        p2 = {'name': 'product2',
              'category': category,
              'description': 'test',
              'price': 120,
              'coast': 120,
              'discount': 0,
              'digital': True,
              'image': test_image_upload,
              'slug': 'product2'}
        p3 = {'name': 'product3',
              'category': category,
              'description': 'test',
              'price': 90,
              'coast': 100,
              'discount': 0,
              'digital': True,
              'image': test_image_upload,
              'slug': 'product3'}
        p4 = {'name': 'product4',
              'category': category,
              'description': 'test',
              'price': 120,
              'coast': 100,
              'discount': 110,
              'digital': True,
              'image': test_image_upload,
              'slug': 'product4'}
        p5 = {'name': 'product5',
              'category': category,
              'description': 'test',
              'price': 120,
              'coast': 100,
              'discount': 300,
              'digital': True,
              'image': test_image_upload,
              'slug': 'product5'}

        self.P1 = Product.objects.create(**p1)
        self.P2 = Product.objects.create(**p2)
        self.P3 = Product.objects.create(**p3)
        self.P4 = Product.objects.create(**p4)
        self.P5 = Product.objects.create(**p5)

    def test_user_string_representation(self):
        user = User(username="tester")
        self.assertEqual(str(user), user.username)

    def test_products_count(self):
        p = Product.objects.all()
        self.assertEqual(p.count(), 5)

    def test_product_string_representation(self):
        product = Product(name="product1")
        self.assertEqual(str(product), product.name)

    def test_valid_product_1(self):
        p1 = Product.objects.get(name='product1')
        self.assertTrue(p1.is_valid_product())

    def test_valid_product_2(self):
        p2 = Product.objects.get(name='product2')
        self.assertFalse(p2.is_valid_product())

    def test_valid_product_3(self):
        p3 = Product.objects.get(name='product3')
        self.assertFalse(p3.is_valid_product())

    def test_valid_product_4(self):
        p4 = Product.objects.get(name='product4')
        self.assertTrue(p4.is_valid_product())

    def test_valid_product_5(self):
        p5 = Product.objects.get(name='product5')
        self.assertFalse(p5.is_valid_product())

    def delete_products_images(self):
        """
        Deletes the uploaded by create_cat_and_product() product image.
        """
        self.P1.image.delete()
        self.P2.image.delete()
        self.P3.image.delete()
        self.P4.image.delete()
        self.P5.image.delete()

    def test_index(self):
        # Set up client to make requests
        c = Client()

        # Send get request to index page and store response
        response = c.get("//")

        # Make sure status code is 200
        self.assertEqual(response.status_code, 200)

        # Make sure three flights are returned in the context
        self.assertEqual(response.context["products"].count(), 5)

    def test_valid_product_page(self):
        p1 = Product.objects.get(name='product1')
        c = Client()
        response = c.get(f"//{p1.slug}")
        self.assertEqual(response.status_code, 200)

    def test_valid_user(self):
        user = User(username="tester")
        c = Client()
        response = c.get(f"/accounts/{user.username}")
        self.assertEqual(response.status_code, 302)

    def tearDown(self):
        self.delete_products_images()

    driver.close()


if __name__ == '__main__':
    unittest.main()
