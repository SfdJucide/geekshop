import json
import os

from django.shortcuts import render

from baskets.models import Basket
from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def index(request):
    context = {
        "title": 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page=1):
    context = {
        "title": 'GeekShop - Каталог',
        "categories_list": ProductCategory.objects.all(),
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
