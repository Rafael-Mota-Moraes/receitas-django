from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'recipes/home.html', status=404, context={
        'name': 'Rafael Moreira'
    })


def sobre(request):
    return HttpResponse('SOBRE')


def contato(request):
    return render(request, 'recipes/contato.html')


# Create your views here.
