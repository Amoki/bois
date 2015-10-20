# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0008_auto_20151013_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='next',
            name='rules',
        ),
        migrations.RemoveField(
            model_name='rule',
            name='next',
        ),
        migrations.AddField(
            model_name='game',
            name='turn_number',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='turn',
            name='number',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='turn',
            name='players',
            field=models.ManyToManyField(to='vomito.Player'),
        ),
        migrations.DeleteModel(
            name='Next',
        ),
    ]
