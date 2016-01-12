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
            if deployment.push_set.all().count() < KEEP:
                # skip any that have 0 or 1 pushes
                continue
            for push in list(deployment.push_set.all().order_by(
                    '-start_time'))[KEEP:]:
                push.delete()
                deleted += 1
            idx += 1
        print("deleted %d" %d deleted)
