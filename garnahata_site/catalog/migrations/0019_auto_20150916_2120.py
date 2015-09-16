# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_auto_20150803_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownership',
            name='mortgage_details',
            field=models.TextField(verbose_name='Деталі за іпотекою', blank=True),
        ),
        migrations.AlterField(
            model_name='ownership',
            name='mortgage_registered',
            field=models.DateTimeField(null=True, verbose_name='Дата реєстрації іпотеки', blank=True),
        ),
    ]
