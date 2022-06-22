from show.models import Show
from rest_framework import serializers


class ShowListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Show
        fields = [
            'pk',
            'show_type',
            'title',
            'director',
            'cast',
        ]

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
