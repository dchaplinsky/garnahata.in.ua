# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_address_date_added'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='cadastral_number',
            field=models.CharField(blank=True, verbose_name='Кадастровий номер', max_length=25, validators=[django.core.validators.RegexValidator(regex='^\\d{10}:\\d{2}:\\d{3}:0000$', message='Кадастровий код не задовільняє формату')]),
            preserve_default=True,
        ),
    ]
