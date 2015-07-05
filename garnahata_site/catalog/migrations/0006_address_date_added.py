# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20150705_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата додання на сайт'),
            preserve_default=True,
        ),
    ]
