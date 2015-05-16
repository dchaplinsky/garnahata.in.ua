# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djgeojson.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('address', models.TextField(verbose_name='Адреса')),
                ('city', models.CharField(max_length=50, verbose_name='Місто')),
                ('commercial_name', models.CharField(blank=True, max_length=150, verbose_name='Назва комплексу або району')),
                ('link', models.URLField(verbose_name='Посилання на сайт забудовника')),
                ('coords', djgeojson.fields.PointField(blank=True, verbose_name='Позиція на мапі')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ownership',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('owner', models.TextField(verbose_name='Власник')),
                ('registered', models.DateTimeField(null=True, blank=True, verbose_name='Реєстрація')),
                ('asset', models.TextField(verbose_name='Власність')),
                ('comment', models.TextField(blank=True, verbose_name='Коментар')),
                ('mortgage', models.TextField(blank=True, verbose_name='Іпотека')),
                ('address', models.ForeignKey(to='catalog.Address', verbose_name='Адреса')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
