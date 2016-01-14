from django.core.management.base import BaseCommand
from rolf.rolf_main.models import Deployment

KEEP = 20


class Command(BaseCommand):
    def handle(self, **options):
        count = Deployment.objects.all().count()
        idx = 1
        deleted = 0
        for deployment in Deployment.objects.all():
            print("[%02d/%02d]" % (idx, count))
            deleted += deployment.clear_old_pushes(keep=KEEP)
            idx += 1
        print("deleted %d" % deleted)
