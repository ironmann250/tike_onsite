# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-11-25 00:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='badges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_name', models.CharField(max_length=100)),
                ('Last_namee', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('Picture', models.ImageField(null=True, upload_to=b'media/profiles')),
            ],
        ),
    ]
