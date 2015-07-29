# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
from catalog.models import Address, Ownership
from catalog.elastic_models import (
    Address as ElasticAddress,
    Ownership as ElasticOwnership
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        ElasticAddress.init()

        Address.objects.all().reindex()

        self.stdout.write(
            'Loaded {} addresses to persistence storage'.format(
                Address.objects.count()))

        ElasticOwnership.init()
        Ownership.objects.all().reindex()

        self.stdout.write(
            'Loaded {} ownerships to persistence storage'.format(
                Ownership.objects.count()))
