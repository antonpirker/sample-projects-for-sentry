from django.http import HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def root(request):
    context = {}
    if request.method == 'POST':
        f = open("/tmp/bla.jpg", "wb")
        f.write(request.FILES["file"].read())
        f.close()

    #bla = 1/0
    return render(request, 'root.html', context)
