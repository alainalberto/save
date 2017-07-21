# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20170710_0151'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ifta',
            old_name='state',
            new_name='period',
        ),
        migrations.RemoveField(
            model_name='ifta',
            name='gallons',
        ),
        migrations.RemoveField(
            model_name='ifta',
            name='milles',
        ),
        migrations.RemoveField(
            model_name='ifta',
            name='trucks',
        ),
        migrations.AddField(
            model_name='ifta',
            name='nex_period',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='ifta',
            name='type',
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name='ifta',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
