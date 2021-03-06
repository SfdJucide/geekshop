from baskets.models import Basket


def basket(request):
    basket_items = []
    if request.user.is_authenticated:
        return Basket.objects.filter(user=request.user)

    return {
        'basket': basket_items
    }