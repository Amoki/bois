# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bois.fields.script_field


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0007_auto_20150904_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='sex',
            field=models.CharField(choices=[('m', '♂'), ('f', '♀')], default='m', max_length=1),
        ),
        migrations.AlterField(
            model_name='rule',
            name='mixte',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rule',
            name='on_proc',
            field=bois.fields.script_field.ScriptField(blank=True, help_text="Called just after the turn is created. `rule` is the pending rule, available without any context (you can't call `set_value`). `game` is the pending game. `turn` is the current turn. `players` is the list of players. `involved_players` is the list of players of this turn.", null=True),
        ),
        migrations.AlterField(
            model_name='turn',
            name='game',
            field=models.ForeignKey(to='vomito.Game'),
        ),
        migrations.AlterUniqueTogether(
            name='player',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='player',
            name='last_name',
        ),
    ]
