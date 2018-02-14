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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=80)),
                ('Country', models.CharField(default='', max_length=20)),
                ('Website', models.URLField(default='', blank=True)),
                ('Email', models.EmailField(default='', max_length=254, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=200)),
            ],
            options={
                'ordering': ('Name',),
                'verbose_name': 'Charity',
                'verbose_name_plural': 'Charities',
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
    ]
