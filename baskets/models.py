from django.db import models

from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Basket for {self.user.username} | Product {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def total_sum(self):
        total_bask = (bask.sum() for bask in Basket.objects.filter(user=self.user))
        return sum(total_bask)

    def total_count(self):
        total_count = (bask.quantity for bask in Basket.objects.filter(user=self.user))
        return sum(total_count)
