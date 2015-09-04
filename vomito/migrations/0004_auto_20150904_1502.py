# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0003_auto_20150904_1329'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='weight',
            new_name='difficulty',
        ),
        migrations.RenameField(
            model_name='rule',
            old_name='name',
            new_name='description',
        ),
        migrations.AddField(
            model_name='category',
            name='weighting',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='mixte',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='player',
            name='sex',
            field=models.CharField(default=b'm', max_length=1, choices=[(b'm', b'\xe2\x99\x82'), (b'f', b'\xe2\x99\x80')]),
        ),
        migrations.AddField(
            model_name='turn',
            name='game',
            field=models.ForeignKey(default=1, to='vomito.Game'),
            preserve_default=False,
        ),
    ]
