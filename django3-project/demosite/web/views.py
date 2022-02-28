import os

from django.shortcuts import render


def index(request):
    context = {}

    from web.tasks import some_actual_task

    some_actual_task.delay(2, 2)
    some_actual_task.delay(2, 20)

    return render(request, "index.html", context)
