# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-06 17:15
from __future__ import unicode_literals

from django.db import migrations


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
    ]
