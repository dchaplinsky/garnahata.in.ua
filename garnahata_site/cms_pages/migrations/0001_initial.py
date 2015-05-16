# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import wagtail.wagtailcore.fields
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0010_change_page_owner_to_null_on_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, parent_link=True, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(verbose_name='Текст сторінки')),
            ],
            options={
                'verbose_name': 'Головна сторінка',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePageTopMenuLink',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('caption', models.CharField(blank=True, max_length=255)),
                ('link_external', models.URLField(blank=True, verbose_name='External link')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawHTMLPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, parent_link=True, to='wagtailcore.Page')),
                ('body', models.TextField(verbose_name='Текст сторінки')),
            ],
            options={
                'verbose_name': 'Raw-HTML сторінка',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, serialize=False, primary_key=True, parent_link=True, to='wagtailcore.Page')),
                ('body', wagtail.wagtailcore.fields.RichTextField(verbose_name='Текст сторінки')),
            ],
            options={
                'verbose_name': 'Статична сторінка',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AddField(
            model_name='homepagetopmenulink',
            name='link_page',
            field=models.ForeignKey(to='wagtailcore.Page', related_name='+', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='homepagetopmenulink',
            name='page',
            field=modelcluster.fields.ParentalKey(to='cms_pages.HomePage', related_name='top_menu_links'),
            preserve_default=True,
        ),
    ]
