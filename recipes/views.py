from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Rafael Moreira'
    })


def recipe(request, id):
    return render(request, 'recipes/pages/home.html', context={
        'name': 'Rafael Moreira'
    })
