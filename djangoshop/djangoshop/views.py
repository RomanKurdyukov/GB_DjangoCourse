from django.shortcuts import render

from mainapp.models import *

def index(request):
    title = 'Магазин'

    products = Product.objects.all()[:4]

    context = {
        'title': title,
        'products': products,
    }
    return render(request, 'djangoshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    context = {
        'title': title,
    }
    return render(request, 'djangoshop/contact.html', context)


