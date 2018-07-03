# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from elasticsearch_dsl import Index
from elasticsearch_dsl.connections import connections


from catalog.models import Address, Ownership
from catalog.elastic_models import (
    Address as ElasticAddress,
    Ownership as ElasticOwnership,
    ownership_idx
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        Index(ElasticAddress._doc_type.index).delete(ignore=404)
        ElasticAddress.init()

        es = connections.get_connection('default')
        es.indices.put_settings(
            index=ElasticAddress._doc_type.index,
            body={
                "number_of_replicas": 0,
                'index.max_result_window': 50000
            }
        )

        Address.objects.reindex()

        self.stdout.write(
            'Loaded {} addresses to persistence storage'.format(
                Address.objects.count()))

        ownership_idx.delete(ignore=404)
        ownership_idx.create()
        ElasticOwnership.init()
        Ownership.objects.select_related("prop__address").reindex()

        self.stdout.write(
            'Loaded {} ownerships to persistence storage'.format(
                Ownership.objects.count()))
