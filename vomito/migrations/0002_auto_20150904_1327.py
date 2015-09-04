# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='Players',
        ),
        migrations.AlterField(
            model_name='rule',
            name='next',
            field=models.ForeignKey(blank=True, to='vomito.Next', null=True),
        ),
    ]
