# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0009_auto_20151019_1403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rule',
            name='max_sip',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='min_sip',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
