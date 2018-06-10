# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields
import modelcluster.contrib.taggit


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('cms_pages', '0008_auto_20150722_0108'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsPageTag',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='blogpagetag',
            name='content_object',
        ),
        migrations.RemoveField(
            model_name='blogpagetag',
            name='tag',
        ),
        migrations.AlterField(
            model_name='newspage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(verbose_name='Tags', blank=True, through='cms_pages.NewsPageTag', help_text='A comma-separated list of tags.', to='taggit.Tag'),
        ),
        migrations.DeleteModel(
            name='BlogPageTag',
        ),
        migrations.AddField(
            model_name='newspagetag',
            name='content_object',
            field=modelcluster.fields.ParentalKey(related_name='tagged_items', to='cms_pages.NewsPage'),
        ),
        migrations.AddField(
            model_name='newspagetag',
            name='tag',
            field=models.ForeignKey(related_name='cms_pages_newspagetag_items', to='taggit.Tag', on_delete=models.CASCADE),
        ),
    ]
