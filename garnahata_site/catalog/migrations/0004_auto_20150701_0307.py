# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20150517_0225'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('address', models.ForeignKey(to='catalog.Address', verbose_name='Адреса')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ownership',
            name='address',
        ),
        migrations.RemoveField(
            model_name='ownership',
            name='mortgage',
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_charge',
            field=models.TextField(verbose_name='Підстава обтяження', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_charge_subjects',
            field=models.TextField(verbose_name="Суб'єкти обтяження", blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_details',
            field=models.TextField(verbose_name='Деталі за іпотекой', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_guarantor',
            field=models.TextField(verbose_name='Власник або іпотекодавець', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_holder',
            field=models.TextField(verbose_name='Заявник або іпотекодержатель', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_mortgagor',
            field=models.TextField(verbose_name='Власник або іпотекодавець', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='mortgage_registered',
            field=models.DateTimeField(null=True, verbose_name='Дата реєстрації іпотекі', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='ownership_form',
            field=models.TextField(verbose_name='Форма власності', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='ownership_ground',
            field=models.TextField(verbose_name='Підстава власності', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ownership',
            name='prop',
            field=models.ForeignKey(verbose_name='Власність', default=None, to='catalog.Property'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ownership',
            name='share',
            field=models.TextField(verbose_name='Частка', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownership',
            name='asset',
            field=models.TextField(verbose_name='Властивості нерухомості'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ownership',
            name='registered',
            field=models.DateTimeField(null=True, verbose_name='Дата реєстрації', blank=True),
            preserve_default=True,
        ),
    ]
