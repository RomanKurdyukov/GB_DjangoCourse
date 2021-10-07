from django.shortcuts import render


def index(request):
    return render(request, 'djangoshop/index.html')


def contacts(request):
    return render(request, 'djangoshop/contact.html')

