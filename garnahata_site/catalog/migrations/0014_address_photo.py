# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_auto_20150720_0158'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='photo',
            field=models.ImageField(blank=True, upload_to='images', verbose_name="Фото об'єкта"),
        ),
    ]
