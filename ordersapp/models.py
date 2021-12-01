from django.db import models
from django.conf import settings

from products.models import Product


class OrderQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for object in self:
            for item in object.orderitems.select_related():
                item.product.quantity += item.quantity
                item.product.save()
            object.is_active = False
            object.save()
        super().delete(*args, **kwargs)


class Order(models.Model):
    objects = OrderQuerySet.as_manager()

    STATUS_FORMING = 'FM'
    STATUS_SEND_TO_PROCEED = 'STP'
    STATUS_PROCEEDED = 'PRD'
    STATUS_PAID = 'PD'
    STATUS_DONE = 'DN'
    STATUS_CANCELED = 'CN'

    STATUSES = (
        (STATUS_FORMING, 'Forming'),
        (STATUS_SEND_TO_PROCEED, 'Send to proceed'),
        (STATUS_PROCEEDED, 'Proceeded'),
        (STATUS_PAID, 'Paid'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELED, 'Canceled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=STATUS_FORMING, max_length=3)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.product.price, items)))

    def delete(self, *args):
        for item in self.orderitems.all():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Count')

    @property
    def get_product_cost(self):
        return self.product.price * self.quantity
