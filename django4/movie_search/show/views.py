from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    bla = 1/0
    return HttpResponse("Hello, world. You're at the SHOW index.")
