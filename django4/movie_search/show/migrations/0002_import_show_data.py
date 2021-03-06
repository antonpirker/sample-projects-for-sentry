# Generated by Django 4.0.5 on 2022-06-21 19:06

from django.db import migrations
from django.conf import settings

import csv

SHOW_TYPE = 1
TITLE = 2
DIRECTOR = 3
CAST = 4
COUNTRIES = 5
DATE_ADDED = 6
RELEASE_YEAR = 7
RATING = 8
DURATION = 9
CATEGORIES = 10
DESCRIPTION = 11

def load_show_data(apps, schema_editor):
    Show = apps.get_model('show', 'Show')

    with open(settings.DATA_DIR / 'netflix_titles.csv', newline='') as csvfile:
        pokemon_reader = csv.reader(csvfile, delimiter=',')
        next(pokemon_reader)  # skip first row
        for row in pokemon_reader:
            Show.objects.create(
                show_type=row[SHOW_TYPE],
                title=row[TITLE],
                director=row[DIRECTOR],
                cast=row[CAST],
                countries=row[COUNTRIES],
                date_added=row[DATE_ADDED],
                release_year=row[RELEASE_YEAR],
                rating=row[RATING],
                duration=row[DURATION],
                categories=row[CATEGORIES],
                description=row[DESCRIPTION],
            )

class Migration(migrations.Migration):

    dependencies = [
        ('show', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_show_data, reverse_code=migrations.RunPython.noop),
    ]
