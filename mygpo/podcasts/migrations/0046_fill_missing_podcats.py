from django.db import migrations
from mygpo.data.tasks import update_podcasts

from mygpo.subscriptions.models import Subscription


def forwards_func(apps, schema_editor):
    podcasts_urls = [
        sub.ref_url for sub in Subscription.objects.filter(podcast__link=None)
    ]
    update_podcasts(podcasts_urls)


def reverse_func(apps, schema_editor):
    """No way to reverse this"""


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("podcasts", "0045_auto_20191230_2330"),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
