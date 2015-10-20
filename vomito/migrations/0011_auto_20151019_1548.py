# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bois.fields.script_field


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0010_auto_20151019_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='next',
            field=models.ForeignKey(to='vomito.Rule', null=True),
        ),
        migrations.AlterField(
            model_name='rule',
            name='on_proc',
            field=bois.fields.script_field.ScriptField(help_text='Called just after the turn is created. `rule` is the pending rule. `game` is the pending game. `turn` is the current turn. `players` is the list of players. `involved_players` is the list of players of this turn. `nb_sip` is the number of sips randomized for this turn.', blank=True, null=True),
        ),
    ]
