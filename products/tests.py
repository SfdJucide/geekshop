from django.test import TestCase
from django.test.client import Client
from products.models import Product, ProductCategory


class TestMainappSmoke(TestCase):

    def setUp(self) -> None:
        self.category = ProductCategory.objects.create(name='cat1')

        for i in range(10):
            Product.objects.create(
                name = f'prod-{i}',
                description = 'desc',
                category = self.category
            )
        self.client = Client()

    def test_main_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_products_urls(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
