# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-06 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='timestamp',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='events',
            old_name='event_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='events',
            name='line_up',
            field=models.CharField(default=1, max_length=10000),
            preserve_default=False,
        ),
    ]
