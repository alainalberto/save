# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 22:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0002_auto_20170509_2351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoices',
            name='date_start',
        ),
        migrations.AddField(
            model_name='invoices',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='accountdescrip',
            name='value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='accounts_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounting.Accounts'),
        ),
        migrations.AlterField(
            model_name='fee',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='invoices',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoiceshasitems',
            name='value_ind',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
