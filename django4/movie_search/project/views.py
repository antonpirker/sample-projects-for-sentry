from django.http import HttpResponse
from django.shortcuts import render


def root(request):
    return HttpResponse("This is the root of everything.")
