from django.shortcuts import render

from products.models import Product


def handler500(request):
    return render(request, '500.html', status=500)


def home(request):
    products = Product.objects.all().count()

    context = {
        'products': products
    }

    return render(request, 'home.html', context)
