# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_address_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='description',
            field=tinymce.models.HTMLField(default='', blank=True, verbose_name="Опис об'єкта"),
        ),
    ]
