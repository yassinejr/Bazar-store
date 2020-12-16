import os
import unittest

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from .models import Product, Category
from bazar import settings
from django.core.files.images import ImageFile


class ProductTestCase(TestCase):
    """
    Contains helper methods, used on many places
    by other classes.
    """

    def setUp(self):
        # create user
        user = {
            'first_name': 'Tester',
            'last_name': 'Testing',
            'username': 'tester',
            'password': 'topsecret2020',
        }
        User.objects.create(**user)

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
              # 'digital': True,
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

    def tearDown(self):
        self.delete_products_images()


if __name__ == '__main__':
    unittest.main()
