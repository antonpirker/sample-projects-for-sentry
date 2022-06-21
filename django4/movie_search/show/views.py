
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from rest_framework.response import Response

from show.models import Show
from show.serializers import ShowSerializer


def index(request):
    bla = 1/0
    return HttpResponse("Hello, world. You're at the SHOW index.")


class ShowViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows shows to be viewed or edited.
    """
    queryset = Show.objects.all().order_by('title')
    serializer_class = ShowSerializer
