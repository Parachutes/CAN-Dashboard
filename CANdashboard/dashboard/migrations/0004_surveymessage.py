# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('directmessaging', '0001_initial'),
        ('forms', '0002_auto_20160418_0120'),
        ('dashboard', '0003_auto_20180305_2254'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyMessage',
            fields=[
                ('message_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='directmessaging.Message')),
                ('survey', models.ForeignKey(to='forms.Form')),
            ],
            bases=('directmessaging.message',),
        ),
    ]
