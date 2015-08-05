# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0014_address_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='description',
            field=tinymce.models.HTMLField(verbose_name="Опис об'єкта", default=''),
        ),
    ]
