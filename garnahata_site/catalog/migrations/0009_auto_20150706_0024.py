# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_auto_20150705_2333'),
    ]

    operations = [
        migrations.AddField(
            model_name='ownership',
            name='mortgage_other_persons',
            field=models.TextField(blank=True, verbose_name="Інші суб'єкти обтяження"),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownership',
            name='mortgage_guarantor',
            field=models.TextField(blank=True, verbose_name='Поручитель'),
            preserve_default=True,
        ),
    ]
