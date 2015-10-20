# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reporting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scriptlog',
            name='direct_queries',
            field=models.PositiveIntegerField(help_text='Number of direct queries or None.', null=True, default=None),
        ),
        migrations.AlterField(
            model_name='scriptlog',
            name='queries',
            field=models.PositiveIntegerField(help_text='Total number of queries, including stack or None.', null=True, default=None),
        ),
        migrations.AlterField(
            model_name='scriptlog',
            name='stack_level',
            field=models.PositiveIntegerField(help_text='Number of calls before this one in the stack.'),
        ),
        migrations.AlterField(
            model_name='scriptlog',
            name='time',
            field=models.PositiveIntegerField(help_text='Time to run, in milliseconds.'),
        ),
    ]
