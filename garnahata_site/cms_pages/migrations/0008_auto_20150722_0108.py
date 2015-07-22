# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('cms_pages', '0007_auto_20150721_2318'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('content_object', modelcluster.fields.ParentalKey(to='cms_pages.NewsPage', related_name='tagged_items')),
                ('tag', models.ForeignKey(to='taggit.Tag', related_name='cms_pages_blogpagetag_items')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='newspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(through='cms_pages.BlogPageTag', help_text='A comma-separated list of tags.', blank=True, to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
