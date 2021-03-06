# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-05-23 17:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('poster', models.ImageField(upload_to=b'media/img')),
                ('video', models.FileField(upload_to=b'media/video')),
                ('Description', models.TextField()),
                ('date', models.DateTimeField(verbose_name=b'2018-05-24')),
                ('tickets_no', models.IntegerField(default=0)),
                ('supervisor', models.ForeignKey(default=b'0', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.IntegerField(null=True)),
                ('email', models.EmailField(max_length=254)),
                ('Name', models.CharField(default=b'0', max_length=100)),
                ('pin', models.CharField(max_length=10)),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=b'2018-05-24')),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tickapp.Show')),
                ('seller', models.ForeignKey(default=b'0', null=True, on_delete=django.db.models.deletion.CASCADE, to='tickapp.profile')),
            ],
        ),
        migrations.CreateModel(
            name='tickettype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('tike_type', models.CharField(max_length=50)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickapp.Show')),
            ],
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(default=b'0', null=True, on_delete=django.db.models.deletion.CASCADE, to='tickapp.tickettype'),
        ),
        migrations.AddField(
            model_name='profile',
            name='event',
            field=models.ForeignKey(default=b'0', on_delete=django.db.models.deletion.CASCADE, to='tickapp.Show'),
        ),
        migrations.AddField(
            model_name='profile',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
