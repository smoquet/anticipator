# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-08-03 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_auto_20160707_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='source_id',
            field=models.IntegerField(default='0000000'),
        ),
    ]