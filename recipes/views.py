from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'recipes/pages/home.html', status=404, context={
        'name': 'Rafael Moreira'
    })
