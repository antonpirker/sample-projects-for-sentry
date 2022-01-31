import os

from django.shortcuts import render

def index(request):
    context = {
        'is_wunderpreview': os.environ.get('IS_WUNDERPREVIEW'),
    }
    return render(request, 'index.html', context)
