from django.shortcuts import render
from django.views.decorators.cache import cache_page

from baskets.models import Basket
from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings
# Create your views here.


@cache_page(4200)
def index(request):
    context = {
        "title": 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def get_categories():
    if settings.LOW_CACHE:
        key = 'categories'
        categories = cache.get(key)
        if categories is None:
            categories = ProductCategory.objects.all()
            cache.set(key, categories)
    return ProductCategory.objects.all()


def products(request, category_id=None, page=1):
    context = {
        "title": 'GeekShop - Каталог',
        "categories_list": get_categories,
    }

    if category_id:
        product = Product.objects.filter(category_id=category_id)
    else:
        product = Product.objects.all()

    paginator = Paginator(product, 3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['product_list'] = products_paginator
    return render(request, 'products/products.html', context)
