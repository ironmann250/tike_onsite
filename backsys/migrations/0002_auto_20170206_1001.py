# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-06 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backsys', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket_type',
            name='amount',
            field=models.IntegerField(max_length=10),
        ),
    ]
