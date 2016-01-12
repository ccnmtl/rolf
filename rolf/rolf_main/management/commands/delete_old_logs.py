from django.core.management.base import BaseCommand
from rolf.rolf_main.models import Deployment
from datetime import datetime, timedelta


class Command(BaseCommand):
    def handle(self, **options):
        now = datetime.now()
        year_ago = now - timedelta(weeks=52)
        count = Deployment.objects.all().count()
        idx = 1
        for deployment in Deployment.objects.all():
            print("[%02d/%02d]" % (idx, count))
            if deployment.push_set.all().count() < 2:
                # skip any that have 0 or 1 pushes
                continue
            most_recent_push = deployment.push_set.all().order_by(
                '-start_time').first()
            deployment.push_set.filter(
                start_time__lt=year_ago,
            ).exclude(id=most_recent_push.id).delete()
