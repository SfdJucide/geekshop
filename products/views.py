import json
import os

from django.shortcuts import render
from products.models import Product

# Create your views here.


def index(request):
    context = {
        "title": 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        "title": 'GeekShop - Каталог',
        "product_list": Product.objects.all()
    }
    return render(request, 'products/products.html', context)
