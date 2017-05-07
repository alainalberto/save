# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-07 04:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_auto_20170505_1807'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alerts',
            old_name='active_alt',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='alerts',
            old_name='category_alt',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='alerts',
            old_name='create_date_alt',
            new_name='create_date',
        ),
        migrations.RenameField(
            model_name='alerts',
            old_name='drescription_alt',
            new_name='drescription',
        ),
        migrations.RenameField(
            model_name='alerts',
            old_name='end_date_alt',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='alerts',
            old_name='show_date_alt',
            new_name='show_date',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='active_bus',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='address_bus',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='date_created_bus',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='date_deactivated_bus',
            new_name='date_deactivated',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='fax_bus',
            new_name='fax',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='logo_bus',
            new_name='logo',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='messager_bus',
            new_name='messager',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='name_bus',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='phone_bus',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='business',
            old_name='website_bus',
            new_name='website',
        ),
        migrations.RenameField(
            model_name='calendar',
            old_name='date_cld',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='calendar',
            old_name='description_cld',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='calendar',
            old_name='title_cld',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='changerusers',
            old_name='name_chg',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='changerusers',
            old_name='value_after_chg',
            new_name='value_after',
        ),
        migrations.RenameField(
            model_name='changerusers',
            old_name='value_before_chg',
            new_name='value_before',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='date_cht',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='chat',
            old_name='messager_cht',
            new_name='messager',
        ),
        migrations.RenameField(
            model_name='directory',
            old_name='address_dir',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='directory',
            old_name='email_dir',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='directory',
            old_name='name_dir',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='directory',
            old_name='phone_dir',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='files',
            old_name='date_save_fil',
            new_name='date_save',
        ),
        migrations.RenameField(
            model_name='files',
            old_name='drescription_fil',
            new_name='drescription',
        ),
        migrations.RenameField(
            model_name='files',
            old_name='name_fil',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='files',
            old_name='url_fil',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='folders',
            old_name='description_fld',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='folders',
            old_name='name_fld',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='histories',
            old_name='acction_hst',
            new_name='acction',
        ),
        migrations.RenameField(
            model_name='histories',
            old_name='date_hst',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='menus',
            old_name='active_men',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='menus',
            old_name='description_men',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='menus',
            old_name='name_men',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='menus',
            old_name='url_men',
            new_name='url',
        ),
        migrations.RenameField(
            model_name='profilers',
            old_name='active_prf',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='profilers',
            old_name='date_deactivated_prf',
            new_name='date_deactivated',
        ),
        migrations.RenameField(
            model_name='profilers',
            old_name='description_prf',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='profilers',
            old_name='name_prf',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='active_use',
            new_name='active',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='date_created_use',
            new_name='date_created',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='date_deactivated_use',
            new_name='date_deactivated',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='email_use',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='lastname_use',
            new_name='lastname',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='name_use',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='online_use',
            new_name='online',
        ),
        migrations.RenameField(
            model_name='users',
            old_name='password_use',
            new_name='password',
        ),
    ]
