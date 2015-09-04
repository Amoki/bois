# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('weight', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sip', models.PositiveIntegerField(null=True)),
                ('bottoms_up', models.NullBooleanField()),
                ('player', models.ForeignKey(to='vomito.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='vomito.Category')),
                ('players', models.ManyToManyField(to='vomito.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Next',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('mixte', models.BooleanField(default=True)),
                ('nb_players', models.PositiveIntegerField()),
                ('category', models.ForeignKey(to='vomito.Category')),
                ('next', models.ForeignKey(to='vomito.Next', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rule', models.ForeignKey(to='vomito.Rule')),
            ],
        ),
        migrations.AddField(
            model_name='next',
            name='rules',
            field=models.ManyToManyField(related_name='+', to='vomito.Rule'),
        ),
        migrations.AddField(
            model_name='drink',
            name='turn',
            field=models.ForeignKey(to='vomito.Turn'),
        ),
        migrations.AlterUniqueTogether(
            name='account',
            unique_together=set([('first_name', 'last_name')]),
        ),
    ]
