# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import cms_pages.models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
        ('wagtailimages', '0005_make_filter_spec_unique'),
        ('cms_pages', '0004_auto_20150702_0255'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPage',
            fields=[
                ('page_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, to='wagtailcore.Page', parent_link=True)),
                ('lead', wagtail.wagtailcore.fields.RichTextField(blank=True, verbose_name='Лід')),
                ('body', wagtail.wagtailcore.fields.RichTextField(verbose_name='Текст новини')),
                ('date_added', models.DateTimeField(verbose_name='Опубліковано')),
                ('reprint', models.BooleanField(verbose_name='Новина не є унікальною', default=False)),
                ('sticky', models.BooleanField(verbose_name='Закріпити новину', default=False)),
                ('important', models.BooleanField(verbose_name='Важлива новина', default=False)),
                ('image', models.ForeignKey(related_name='+', to='wagtailimages.Image', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
            options={
                'verbose_name': 'Новина',
            },
            bases=(cms_pages.models.AbstractJinjaPage, 'wagtailcore.page'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='news_count',
            field=models.IntegerField(verbose_name='Кількість новин на сторінку', default=6),
            preserve_default=True,
        ),
    ]
