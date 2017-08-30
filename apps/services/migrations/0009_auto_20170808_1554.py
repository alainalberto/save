# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-08 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0008_auto_20170724_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='companie',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='driver',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ifta',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='insurance',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='plate',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='trucks',
            name='update',
            field=models.DateField(blank=True, null=True),
        ),
    ]