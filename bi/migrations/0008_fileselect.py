# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-01 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi', '0007_measureselect'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileSelect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=200)),
            ],
        ),
    ]
