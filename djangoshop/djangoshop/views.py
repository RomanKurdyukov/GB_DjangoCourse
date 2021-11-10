from django.shortcuts import render


def index(request):
    title = 'Магазин'

    context = {
        'title': title,
    }
    return render(request, 'djangoshop/index.html', context)


def contacts(request):
    title = 'Контакты'

    context = {
        'title': title,
    }
    return render(request, 'djangoshop/contact.html', context)


