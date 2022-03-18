from django.db import migrations
from mygpo.data.tasks import update_podcasts


def forwards_func(apps, schema_editor):
    Subscription = apps.get_model('subscriptions','Subscription')
    podcasts_urls = [
        sub.ref_url for sub in Subscription.objects.filter(podcast__link=None)
    ]
    update_podcasts(podcasts_urls)


def reverse_func(apps, schema_editor):
    """No way to reverse this"""


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("subscriptions", "0004_subscription_index"),
    ]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
