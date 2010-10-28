"""
imports a csv file of recipes. 

expects the format from dump_cookbook

Use like

./manage.py import_cookbook /path/to/cookbook.csv

"""
from django.core.management.base import BaseCommand, CommandError
import csv
import cStringIO
from rolf_main.models import *

class Command(BaseCommand):
    def handle(self,fname,**options):
        print fname
        reader = csv.reader(open(fname))
        for row in reader:
            if len(row) == 4:
                r = Recipe.objects.create(name=row[0],
                                          language=row[1],
                                          code=row[2],
                                          description=row[3])

