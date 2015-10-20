# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0012_auto_20151019_1600'),
    ]

    operations = [
        migrations.RenameField(
            model_name='drink',
            old_name='bottoms_up',
            new_name='bottom_up',
        ),
        migrations.RemoveField(
            model_name='game',
            name='turn_number',
        ),
        migrations.AddField(
            model_name='game',
            name='current_turn',
            field=models.ForeignKey(related_name='current_turn', null=True, to='vomito.Turn'),
        ),
        migrations.AlterUniqueTogether(
            name='turn',
            unique_together=set([('game', 'number')]),
        ),
    ]
