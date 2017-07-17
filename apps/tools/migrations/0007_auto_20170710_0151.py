# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 06:51
from __future__ import unicode_literals

import apps.services.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0006_auto_20170709_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='date_save',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='file',
            name='url',
            field=models.FileField(blank=True, null=True, upload_to='Forms/', validators=[apps.services.validators.validate_file_extension]),
        ),
    ]