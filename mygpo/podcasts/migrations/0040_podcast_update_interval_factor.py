# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('podcasts', '0039_podcast_search_index_uptodate')]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='update_interval_factor',
            field=models.FloatField(default=1),
        )
    ]
