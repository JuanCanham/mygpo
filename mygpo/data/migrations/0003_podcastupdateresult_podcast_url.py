# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-03 17:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('data', '0002_result_podcast_null')]

    operations = [
        migrations.AddField(
            model_name='podcastupdateresult',
            name='podcast_url',
            field=models.URLField(default='unknown', max_length=2048),
            preserve_default=False,
        )
    ]
