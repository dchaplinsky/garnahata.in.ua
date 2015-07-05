# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_auto_20150701_0307'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='cadastral_number',
            field=models.TextField(blank=True, verbose_name='Кадастровий номер', validators=[django.core.validators.RegexValidator(message='Кадастровий код не задовільняє формату', regex='^\\d{10}:\\d{2}:\\d{3}:0000$')]),
            preserve_default=True,
        ),

        migrations.RemoveField(
            model_name='address',
            name='city'
        ),

        migrations.AddField(
            model_name='address',
            name='city',
            field=models.IntegerField(verbose_name='Місто', default=80, choices=[(1, 'Сімферополь'), (71, 'Черкаси'), (68, 'Хмельницький'), (5, 'Вінниця'), (65, 'Херсон'), (73, 'Чернівці'), (74, 'Чернігів'), (12, 'Дніпропетровськ'), (14, 'Донецьк'), (80, 'Київ'), (18, 'Житомир'), (21, 'Ужгород'), (23, 'Запоріжжя'), (26, 'Івано-Франківськ'), (32, 'Київ'), (35, 'Кіровоград'), (7, 'Луцьк'), (44, 'Луганськ'), (46, 'Львів'), (48, 'Миколаїв'), (51, 'Одеса'), (53, 'Полтава'), (56, 'Рівне'), (59, 'Суми'), (61, 'Тернопіль'), (85, 'Севастополь'), (63, 'Харків')], max_length=50),
            preserve_default=True,
        ),
    ]
