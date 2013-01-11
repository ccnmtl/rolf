"""
dumps the current recipes in the cookbook out to a CSV file
(to STDOUT). Use like:

./manage.py dump_cookbook > /path/to/cookbook.csv

The format will be readable by the 'import_cookbook' command.

"""
from django.core.management.base import BaseCommand
import csv
import cStringIO
from rolf_main.models import Recipe


class Command(BaseCommand):
    def handle(self, **options):
        sio = cStringIO.StringIO()
        w = csv.writer(sio)
        for recipe in Recipe.objects.all().exclude(name=""):
            w.writerow([recipe.name, recipe.language, recipe.code,
                        recipe.description])
        print sio.getvalue()
