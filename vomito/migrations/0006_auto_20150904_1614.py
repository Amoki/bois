# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bois.fields.script_field


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0005_rule_on_proc'),
    ]

    operations = [
        migrations.AddField(
            model_name='turn',
            name='string',
            field=models.TextField(default='azert'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rule',
            name='on_proc',
            field=bois.fields.script_field.ScriptField(help_text=b"Called just after the turn is created. `rule` is the pending rule, available without any context (you can't call `set_value`). `game` is the pending game. `turn` is the current turn. `players` is the list of players", null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='turn',
            name='game',
            field=models.ForeignKey(related_name='current_turn', to='vomito.Game'),
        ),
    ]
