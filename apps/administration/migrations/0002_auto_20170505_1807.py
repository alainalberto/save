# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-05 23:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alerts',
            name='profilers',
            field=models.ManyToManyField(blank=True, to='administration.Profilers'),
        ),
        migrations.AlterField(
            model_name='alerts',
            name='users',
            field=models.ForeignKey(db_column='USERS_id_use', on_delete=django.db.models.deletion.CASCADE, to='administration.Users'),
        ),
        migrations.AlterField(
            model_name='calendar',
            name='users',
            field=models.ForeignKey(db_column='USERS_id_use', on_delete=django.db.models.deletion.CASCADE, to='administration.Users'),
        ),
        migrations.AlterField(
            model_name='changerusers',
            name='histories',
            field=models.ForeignKey(db_column='HISTORIES_id_hst', on_delete=django.db.models.deletion.CASCADE, to='administration.Histories'),
        ),
        migrations.AlterField(
            model_name='chat',
            name='users',
            field=models.ForeignKey(db_column='USERS_id_use', on_delete=django.db.models.deletion.CASCADE, to='administration.Users'),
        ),
        migrations.AlterField(
            model_name='directory',
            name='users',
            field=models.ForeignKey(db_column='USERS_id_use', on_delete=django.db.models.deletion.CASCADE, to='administration.Users'),
        ),
        migrations.AlterField(
            model_name='files',
            name='folders',
            field=models.ForeignKey(db_column='FOLDERS_id_fld', on_delete=django.db.models.deletion.CASCADE, to='administration.Folders'),
        ),
        migrations.AlterField(
            model_name='files',
            name='users',
            field=models.ForeignKey(db_column='USERS_id_use', on_delete=django.db.models.deletion.CASCADE, to='administration.Users'),
        ),
        migrations.AlterField(
            model_name='folders',
            name='folders_id',
            field=models.ForeignKey(db_column='FOLDERS_id_fld', on_delete=django.db.models.deletion.CASCADE, to='administration.Folders'),
        ),
        migrations.AlterField(
            model_name='histories',
            name='users',
            field=models.ForeignKey(db_column='USERS_id_use', on_delete=django.db.models.deletion.CASCADE, to='administration.Users'),
        ),
        migrations.AlterField(
            model_name='menus',
            name='menus_id',
            field=models.ForeignKey(blank=True, db_column='MENUS_id_men', null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.Menus'),
        ),
        migrations.AlterField(
            model_name='profilers',
            name='menus',
            field=models.ManyToManyField(blank=True, to='administration.Menus'),
        ),
        migrations.AlterField(
            model_name='users',
            name='profilers',
            field=models.ForeignKey(db_column='PROFILERS_id_prf', on_delete=django.db.models.deletion.CASCADE, to='administration.Profilers'),
        ),
    ]
