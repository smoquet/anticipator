# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-09 20:17
from __future__ import unicode_literals

from django.db import migrations
import form.models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='line_up',
            field=form.models.SeparatedValuesField(default='bla'),
            preserve_default=False,
        ),
    ]
