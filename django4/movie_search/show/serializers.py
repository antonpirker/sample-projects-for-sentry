from show.models import Show
from rest_framework import serializers


class ShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = [
            'pk',
            'show_type',
            'title',
            'director',
            'cast',
            'countries',
            'date_added',
            'release_year',
            'rating',
            'duration',
            'categories',
            'description',
        ]
