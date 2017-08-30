# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-30 05:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0008_auto_20170829_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='start_date',
            field=models.DateField(default='2017-08-30'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='files',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tools.File'),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='start_date',
            field=models.DateField(default='2017-08-30'),
        ),
    ]