import random

from django.shortcuts import render, get_object_or_404

from mainapp.models import *


def get_hot_prod():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_prod(hot_prod):
    same_products = Product.objects.filter(category=hot_prod.category).exclude(pk=hot_prod.pk)[:4]
    return same_products


def products(request, pk=None):
    title = 'Каталог'
    links_menu = ProductCategory.objects.all()
    products = Product.objects.all().order_by('price')[:4]

    if pk is not None:
        if pk == 0:
            products = Product.objects.select_related('image').filter(
                is_active=True,
                category__is_active=True,
                quantity__gte=1
            ).order_by('price')[:4]
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(
                category__pk=pk,
                is_active=True,
                category__is_active=True,
                quantity__gte=1
            ).order_by('price')[:4]

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
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
    }
    return render(request, 'mainapp/product.html', context)
