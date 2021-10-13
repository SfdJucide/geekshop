from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        "title": 'GeekShop',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        "title": 'GeekShop - Каталог',
        "product_list": [
            {"img": 'vendor/img/products/Adidas-hoodie.png',
             "name": 'Худи черного цвета с монограммами adidas Originals',
             "description": "Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.",
             "cost": 6090},

            {"img": 'vendor/img/products/Blue-jacket-The-North-Face.png',
             "name": 'Синяя куртка The North Face',
             "description": "Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.",
             "cost": 23725},

            {"img": 'vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
             "name": 'Коричневый спортивный oversized-топ ASOS DESIGN',
             "description": "Материал с плюшевой текстурой. Удобный и мягкий.",
             "cost": 3390},

            {"img": 'vendor/img/products/Black-Nike-Heritage-backpack.png',
             "name": 'Черный рюкзак Nike Heritage',
             "description": "Плотная ткань. Легкий материал.",
             "cost": 2340},

            {"img": 'vendor/img/products/Black-Dr-Martens-shoes.png',
             "name": 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
             "description": "Гладкий кожаный верх. Натуральный материал.",
             "cost": 13590},

            {"img": 'vendor/img/products/Dark-blue-wide-leg-ASOs-DESIGN-trousers.png',
             "name": 'Темно-синие широкие строгие брюки ASOS DESIGN',
             "description": "Легкая эластичная ткань сирсакер Фактурная ткань.",
             "cost": 2890},
        ]
    }
    return render(request, 'products/products.html', context)

