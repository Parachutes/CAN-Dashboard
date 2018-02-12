# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('Name', models.CharField(max_length=80)),
                ('Country', models.CharField(max_length=20)),
                ('Website', models.URLField()),
                ('Email', models.EmailField(max_length=254, serialize=False, primary_key=True)),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
            options={
                'ordering': ('Name',),
            },
        ),
        migrations.CreateModel(
            name='Charity_details',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Delivery', models.IntegerField(default='0', blank=True)),
                ('Financial_health', models.IntegerField(default='0', blank=True)),
                ('Strength_of_system', models.IntegerField(default='0', blank=True)),
                ('Progress', models.IntegerField(default='0', blank=True)),
                ('Name', models.ForeignKey(to='app.Charity')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Response', models.FloatField()),
                ('Field', models.IntegerField()),
                ('Name', models.ForeignKey(to='app.Charity_details')),
            ],
        ),
    ]
