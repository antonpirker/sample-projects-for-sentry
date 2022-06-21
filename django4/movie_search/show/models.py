from django.db import models

class Show(models.Model):
    show_type = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    cast = models.CharField(max_length=200)
    countries = models.CharField(max_length=200)
    date_added = models.DateTimeField()
    release_year = models.SmallIntegerField()
    rating = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    categories = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
