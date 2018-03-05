# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0002_auto_20160418_0120'),
        ('dashboard', '0002_auto_20180303_1856'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='dashboard.Charity_details')),
                ('question', models.ForeignKey(to='forms.Field')),
            ],
        ),
        migrations.AlterField(
            model_name='charity',
            name='Country',
            field=models.CharField(max_length=20, blank=True),
        ),
    ]
