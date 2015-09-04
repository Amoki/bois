# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import bois.fields.script_field


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0004_auto_20150904_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='rule',
            name='on_proc',
            field=bois.fields.script_field.ScriptField(help_text=b"Called after this mission is created. `param` is the pending mission, available without any context (you can't call `set_value`). Use `stop('some_error')` to abort the mission.", null=True, blank=True),
        ),
    ]
