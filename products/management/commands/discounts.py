from django.db.models import F, Q, When, Case, DecimalField, IntegerField
from datetime import timedelta
from django.core.management.base import BaseCommand

from ordersapp.models import OrderItem


class Command(BaseCommand):

    def handle(self, *args, **options):

        ACTION_1 = 1
        ACTION_2 = 2
        ACTION_3 = 3

        action_1_delta = timedelta(hours=12)
        action_2_delta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__update_at__lte=F('order__created_at') + action_1_delta)

        action_2_condition = Q(
            Q(order__update_at__gt=F('order__created_at') + action_1_delta) &
            Q(order__update_at__lte=F('order__created_at') + action_2_delta))

        action_3_condition = Q(order__update_at__gt=F('order__created_at') + action_2_delta)

        action_1_order = When(action_1_condition, then=ACTION_1)
        action_2_order = When(action_2_condition, then=ACTION_2)
        action_3_order = When(action_3_condition, then=ACTION_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        orders_item_list = OrderItem.objects.all().annotate(
           action_order=Case(
               action_1_order,
               action_2_order,
               action_3_order,
               output_field=IntegerField(),
           )
        ).annotate(
           discount_price=Case(
               action_1_price,
               action_2_price,
               action_3_price,
               output_field=DecimalField(),
           )
        )

        for item in orders_item_list:
           print(f'{item.action_order}: ����� �{item.pk}: {item.product.name}: ������'
                 f' {abs(item.discount_price)} ���. | {item.order.update_at - item.order.created_at}')
