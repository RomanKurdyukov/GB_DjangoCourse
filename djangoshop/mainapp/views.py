import random

from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from mainapp.models import *


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_prod():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_prod(hot_prod):
    same_products = Product.objects.filter(category=hot_prod.category).exclude(pk=hot_prod.pk)[:2]
    return same_products


def products(request, pk=None):
    title = 'Каталог'
    links_menu = ProductCategory.objects.all()
    products = Product.objects.all().order_by('price')
    basket = get_basket(request.user)

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
            'basket': basket
        }

        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_prod()
    same_products = get_same_prod(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
        'products': products,
        'basket': basket
    }

    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    title = 'Описание'

    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': product,
        'same_products': get_same_prod(product),
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/product.html', context)
