# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vomito', '0006_auto_20150904_1614'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScriptLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_type', models.CharField(max_length=100)),
                ('object_pk', models.PositiveIntegerField()),
                ('stack_level', models.PositiveIntegerField(help_text=b'Number of calls before this one in the stack.')),
                ('time', models.PositiveIntegerField(help_text=b'Time to run, in milliseconds.')),
                ('direct_queries', models.PositiveIntegerField(default=None, help_text=b'Number of direct queries or None.', null=True)),
                ('queries', models.PositiveIntegerField(default=None, help_text=b'Total number of queries, including stack or None.', null=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, to='vomito.Game', null=True)),
            ],
        ),
    ]
