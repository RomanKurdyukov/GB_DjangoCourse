from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import *

def index(request):
    title = 'Магазин'
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

    products = Product.objects.all()[:4]

    context = {
        'title': title,
        'products': products,
        'basket': basket,
        'basket_count': basket
    }
    return render(request, 'djangoshop/index.html', context)


def contacts(request):
    title = 'Контакты'
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    else:
        basket = []

    context = {
        'title': title,
        'basket': basket,
        'basket_count': basket
    }
    return render(request, 'djangoshop/contact.html', context)


