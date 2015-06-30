# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20150517_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='link',
            field=models.URLField(max_length=1000, verbose_name='Посилання на сайт забудовника'),
            preserve_default=True,
        ),
    ]
