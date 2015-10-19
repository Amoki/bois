# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0011_auto_20151019_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='randomizable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='next',
            field=models.ForeignKey(to='vomito.Rule', blank=True, null=True),
        ),
    ]
