# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0006_auto_20150904_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='max_sip',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rule',
            name='min_sip',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
    ]
