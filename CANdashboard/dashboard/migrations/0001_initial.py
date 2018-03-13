# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('directmessaging', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forms', '0002_auto_20160418_0120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Name', models.CharField(max_length=80)),
                ('Country', models.CharField(max_length=20, blank=True)),
                ('Website', models.URLField(default='', blank=True)),
                ('Email', models.EmailField(default='', max_length=254, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
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
                ('Name', models.ForeignKey(to='dashboard.Charity')),
            ],
        ),
        migrations.CreateModel(
            name='RelatedQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='dashboard.Charity_details')),
                ('question', models.ForeignKey(to='forms.Field')),
            ],
        ),
        migrations.CreateModel(
            name='SurveyMessage',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='directmessaging.Message')),
                ('survey', models.ForeignKey(to='forms.Form')),
            ],
            bases=('directmessaging.message',),
        ),
    ]
